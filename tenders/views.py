from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Tender, Bid, OrganizationResponsible, Employee
from .serializers import TenderSerializer, BidSerializer
from .permissions import (
    IsOrganizationResponsible,
    IsTenderCreatorOrResponsible
)
from .filters import TenderFilter, BidFilter


def ping(request):
    """Простая проверка работы сервера. Возвращает 'ok'"""
    return HttpResponse("ok", content_type="text/plain")


class BaseTenderBidViewSet(viewsets.ModelViewSet):
    """
    Базовый вьюсет для управления объектами Tender и Bid.
    Содержит общую логику для работы со статусами, версиями и правами доступа
    """
    filter_backends = (DjangoFilterBackend,)

    def get_permissions(self):
        """Определяет права доступа для действий update, delete и create"""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsTenderCreatorOrResponsible()]
        elif self.action == 'create':
            return [IsOrganizationResponsible()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        """
        Создает новый объект (Tender или Bid), проверяя права на организацию
        """
        organization_id = request.data.get('organization')
        creator_id = request.data.get('creator')
        if not OrganizationResponsible.objects.filter(
                user_id=creator_id, organization_id=organization_id
        ).exists():
            return Response({"detail": "Вы не ответственны за организацию"},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Обновляет объект, увеличивая его версию"""
        obj = self.get_object()
        obj.version += 1
        obj.save()
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='new')
    def create_obj(self, request):
        """Создает новый объект"""
        return self.create(request)

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        """
        Обновляет статус объекта (Tender или Bid) и увеличивает его версию
        """
        obj = self.get_object()
        new_status = request.data.get('status')
        if new_status not in ['CREATED', 'PUBLISHED', 'CLOSED']:
            return Response({"detail": "Invalid status."},
                            status=status.HTTP_400_BAD_REQUEST)
        obj.status = new_status
        obj.version += 1
        obj.save()
        return Response({'status': 'status updated'},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='my')
    def list_my_items(self, request):
        """
        Возвращает список объектов (тендеров или предложений), созданных
        текущим пользователем.
        """
        username = request.GET.get('username')
        if not username:
            return Response({"detail": "Username parameter is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Employee.objects.get(username=username)
        except Employee.DoesNotExist:
            return Response({"detail": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)

        queryset = self.queryset.filter(creator=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='edit')
    def edit_obj(self, request, pk=None):
        """Частично обновляет объект по ID"""
        return self.partial_update(request)

    def partial_update(self, request, *args, **kwargs):
        """Частично обновляет объект"""
        return super().partial_update(request, *args, **kwargs)


class TenderViewSet(BaseTenderBidViewSet):
    """Вьюсет для управления тендерами"""

    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    filterset_class = TenderFilter


class BidViewSet(BaseTenderBidViewSet):
    """Вьюсет для управления предложениями"""

    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    filterset_class = BidFilter

    @action(detail=True, methods=['get'], url_path='list')
    def list_bids_for_tender(self, request, pk=None):
        """Возвращает список предложений для указанного тендера"""
        try:
            tender = Tender.objects.get(pk=pk)
        except Tender.DoesNotExist:
            return Response({"detail": "Tender not found."},
                            status=status.HTTP_404_NOT_FOUND)
        bids = Bid.objects.filter(tender=tender)

        serializer = self.get_serializer(bids, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
