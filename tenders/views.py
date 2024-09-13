from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Tender, Bid, OrganizationResponsible, Employee, \
    TenderVersion, BidVersion, Review
from .serializers import TenderSerializer, BidSerializer, ReviewSerializer
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
        """
        Обновляет объект, увеличивая его версию и сохраняет предыдущую версию
        """
        instance = self.get_object()
        self.save_version(instance)
        instance.version += 1
        instance.save()
        return super().update(request, *args, **kwargs)

    def save_version(self, instance):
        """Сохранение текущей версии объекта перед изменением"""
        version_data = {
            'name': instance.name,
            'description': instance.description,
            'status': instance.status,
            'version': instance.version
        }

        if isinstance(instance, Tender):
            TenderVersion.objects.create(
                tender=instance,
                service_type=instance.service_type,
                **version_data
            )
        elif isinstance(instance, Bid):
            BidVersion.objects.create(
                bid=instance,
                **version_data
            )

    @action(detail=True, methods=['put'],
            url_path='rollback/(?P<version>[0-9]+)')
    def rollback(self, request, pk=None, version=None):
        """Откат к указанной версии для тендера или предложения"""
        instance = self.get_object()
        version_number = int(version)

        if version_number >= instance.version or version_number <= 0:
            return Response({"detail": "Invalid version for rollback."},
                            status=status.HTTP_400_BAD_REQUEST)

        if isinstance(instance, Tender):
            version_obj = TenderVersion.objects.filter(
                tender=instance,
                version=version_number
            ).first()
        elif isinstance(instance, Bid):
            version_obj = BidVersion.objects.filter(
                bid=instance,
                version=version_number
            ).first()

        if not version_obj:
            return Response({"detail": "Version not found."},
                            status=status.HTTP_404_NOT_FOUND)

        self.save_version(instance)

        instance.name = version_obj.name
        instance.description = version_obj.description
        instance.status = version_obj.status
        if isinstance(instance, Tender):
            instance.service_type = version_obj.service_type
        instance.version += 1
        instance.save()

        return Response(
            {"detail": f"{instance.__class__.__name__} "
                       f"rolled back to version {version_number}."},
            status=status.HTTP_200_OK
        )

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
        """Частично обновляет объект, увеличивая версию"""
        instance = self.get_object()
        self.save_version(instance)
        instance.version += 1
        instance.save()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class TenderViewSet(BaseTenderBidViewSet):
    """Вьюсет для управления тендерами"""

    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    filterset_class = TenderFilter

    def update(self, request, *args, **kwargs):
        tender = self.get_object()
        TenderVersion.objects.create(
            tender=tender,
            name=tender.name,
            description=tender.description,
            status=tender.status,
            service_type=tender.service_type,
            version=tender.version
        )
        tender.version += 1
        tender.save()
        return super().update(request, *args, **kwargs)


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

    @action(detail=True, methods=['get'], url_path='reviews')
    def list_reviews_for_bid(self, request, pk=None):
        """
        Возвращает список отзывов для предложения, созданного определенным
        автором
        """
        author_username = request.query_params.get('authorUsername')
        organization_id = request.query_params.get('organizationId')

        # Проверяем, что указаны оба параметра
        if not author_username or not organization_id:
            return Response(
                {
                    "detail": "Both authorUsername and organizationId "
                              "are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            bid = Bid.objects.get(pk=pk)
        except Bid.DoesNotExist:
            return Response({"detail": "Bid not found."},
                            status=status.HTTP_404_NOT_FOUND)

        if not OrganizationResponsible.objects.filter(
                user__username=author_username,
                organization_id=organization_id).exists():
            return Response({"detail": "Вы не ответственны за организацию."},
                            status=status.HTTP_403_FORBIDDEN)

        reviews = Review.objects.filter(bid=bid,
                                        author__username=author_username)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='feedback')
    def create_review_for_bid(self, request, pk=None):
        """
        Создает отзыв для предложения (Bid)
        """
        user = request.data.get('authorUsername')
        organization_id = request.data.get('organizationId')

        if not user or not organization_id:
            return Response(
                {
                    "detail":
                        "Both authorUsername and organizationId are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            bid = Bid.objects.get(pk=pk)
        except Bid.DoesNotExist:
            return Response(
                {"detail": "Bid not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not OrganizationResponsible.objects.filter(
                user__username=user,
                organization_id=organization_id
        ).exists():
            return Response(
                {"detail": "Вы не ответственны за организацию."},
                status=status.HTTP_403_FORBIDDEN
            )

        review_content = request.data.get('content')
        if not review_content:
            return Response({"detail": "Review content is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        author = Employee.objects.get(username=user)
        Review.objects.create(bid=bid, author=author, content=review_content)
        return Response({"detail": "Review created successfully"},
                        status=status.HTTP_201_CREATED)
