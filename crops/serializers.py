
from rest_framework import serializers

from .models import Crop, CropListing


class CropListingSerializer(serializers.ModelSerializer):

    crop_name = serializers.CharField(
        source='crop.name',
        read_only=True
    )

    class Meta:
        model = CropListing

        fields = [
            'id',
            'crop',
            'crop_name',
            'quantity',
            'unit',
            'expected_price',
            'state',
            'district',
            'availability_status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'crop_name',
            'created_at',
            'updated_at',
        ]

    def validate_crop(self, value):
        if not Crop.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(
                'The selected crop does not exist.'
            )

        return value
