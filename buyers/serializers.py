
from decimal import Decimal

from rest_framework import serializers

from .models import BuyerProfile
from crops.models import CropListing


class BuyerProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )

    class Meta:
        model = BuyerProfile

        fields = [
            'id',
            'username',
            'email',
            'business_name',
            'phone',
            'address',
            'state',
            'district',
            'buyer_type',
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


class BuyerListingFilterSerializer(serializers.Serializer):

    crop = serializers.CharField(
        required=False,
        max_length=100
    )

    state = serializers.CharField(
        required=False,
        max_length=100
    )

    district = serializers.CharField(
        required=False,
        max_length=100
    )

    unit = serializers.ChoiceField(
        choices=CropListing.Unit.choices,
        required=False
    )

    min_quantity = serializers.DecimalField(
        max_digits=12,
        decimal_places=3,
        min_value=Decimal('0.001'),
        required=False
    )

    max_quantity = serializers.DecimalField(
        max_digits=12,
        decimal_places=3,
        min_value=Decimal('0.001'),
        required=False
    )

    min_expected_price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0'),
        required=False
    )

    max_expected_price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0'),
        required=False
    )

    def validate(self, attrs):

        min_quantity = attrs.get('min_quantity')
        max_quantity = attrs.get('max_quantity')

        if (
            min_quantity is not None
            and max_quantity is not None
            and min_quantity > max_quantity
        ):
            raise serializers.ValidationError({
                'max_quantity':
                    'Maximum quantity cannot be less than minimum quantity.'
            })

        min_price = attrs.get('min_expected_price')
        max_price = attrs.get('max_expected_price')

        if (
            min_price is not None
            and max_price is not None
            and min_price > max_price
        ):
            raise serializers.ValidationError({
                'max_expected_price':
                    'Maximum expected price cannot be less than minimum expected price.'
            })

        return attrs


class BuyerCropListingSerializer(serializers.ModelSerializer):

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

        read_only_fields = fields


class FarmerContactSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        from farmers.models import FarmerProfile

        model = FarmerProfile

        fields = [
            'username',
            'phone',
        ]

        read_only_fields = fields


class BuyerCropListingDetailSerializer(BuyerCropListingSerializer):

    farmer = FarmerContactSerializer(read_only=True)

    class Meta(BuyerCropListingSerializer.Meta):

        fields = BuyerCropListingSerializer.Meta.fields + [
            'farmer',
        ]
