
from rest_framework import serializers

from .models import MarketPrice


class MarketPriceSerializer(serializers.ModelSerializer):

    crop_name = serializers.CharField(
        source='crop.name',
        read_only=True
    )

    class Meta:
        model = MarketPrice
        fields = [
            'id',
            'crop',
            'crop_name',
            'state',
            'district',
            'mandi',
            'variety',
            'minimum_price',
            'maximum_price',
            'modal_price',
            'price_date',
            'source',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields
