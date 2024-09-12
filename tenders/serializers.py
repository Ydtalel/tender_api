from rest_framework import serializers
from .models import Tender, Bid


class TenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = ['id', 'name', 'description', 'organization', 'status',
                  'service_type', 'version', 'creator', 'created_at',
                  'updated_at']


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'name', 'description', 'status', 'version', 'tender',
                  'creator', 'organization', 'created_at', 'updated_at']
