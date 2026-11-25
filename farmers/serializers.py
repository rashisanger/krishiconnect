
from rest_framework import serializers

from .models import FarmerProfile


class FarmerProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )

    class Meta:
        model = FarmerProfile

        fields = [
            'id',
            'username',
            'email',
            'phone',
            'address',
            'state',
            'district',
            'village',
            'pincode',
            'land_area',
            'land_area_unit',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'username',
            'email',
            'created_at',
            'updated_at',
        ]
