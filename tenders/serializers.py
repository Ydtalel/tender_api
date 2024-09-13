from rest_framework import serializers
from .models import Tender, Bid


class BaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для тендеров и предложений"""

    class Meta:
        fields = ['id', 'name', 'description', 'status', 'version', 'creator',
                  'organization', 'created_at', 'updated_at']


class TenderSerializer(BaseSerializer):
    """Сериализатор для тендеров"""

    class Meta(BaseSerializer.Meta):
        model = Tender
        fields = BaseSerializer.Meta.fields + ['service_type']


class BidSerializer(BaseSerializer):
    """Сериализатор для предложений."""

    class Meta(BaseSerializer.Meta):
        model = Bid
