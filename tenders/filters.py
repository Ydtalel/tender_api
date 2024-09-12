import django_filters
from .models import Tender, Bid


class TenderFilter(django_filters.FilterSet):
    """Фильтр для модели тендера. Позволяет фильтровать тендеры по типу услуги
     и статусу
    """

    service_type = django_filters.ChoiceFilter(
        choices=Tender.SERVICE_TYPE_CHOICES)
    status = django_filters.ChoiceFilter(
        choices=Tender.STATUS_CHOICES)

    class Meta:
        model = Tender
        fields = ['service_type', 'status']


class BidFilter(django_filters.FilterSet):
    """Фильтр для модели заявки. Позволяет фильтровать заявки по статусу"""

    status = django_filters.ChoiceFilter(
        choices=Bid.STATUS_CHOICES)

    class Meta:
        model = Bid
        fields = ['status']
