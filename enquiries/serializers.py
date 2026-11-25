
from decimal import Decimal

from rest_framework import serializers

from .models import Enquiry, Offer
from crops.models import CropListing


class EnquiryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = [
            'id',
            'crop_listing',
            'message',
            'requested_quantity',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def validate_crop_listing(self, listing):
        if listing.availability_status != CropListing.AvailabilityStatus.AVAILABLE:
            raise serializers.ValidationError(
                'Enquiries can only be created for available crop listings.'
            )
        return listing

    def validate_requested_quantity(self, quantity):
        if quantity <= Decimal('0'):
            raise serializers.ValidationError(
                'Requested quantity must be greater than zero.'
            )
        return quantity

    def validate(self, attrs):
        listing = attrs.get('crop_listing')
        quantity = attrs.get('requested_quantity')

        if listing and quantity and quantity > listing.quantity:
            raise serializers.ValidationError({
                'requested_quantity':
                    'Requested quantity cannot exceed the listed quantity.'
            })

        return attrs


class EnquiryReadSerializer(serializers.ModelSerializer):
    crop_name = serializers.CharField(
        source='crop_listing.crop.name',
        read_only=True,
    )
    listing_quantity = serializers.DecimalField(
        source='crop_listing.quantity',
        max_digits=12,
        decimal_places=3,
        read_only=True,
    )
    listing_unit = serializers.CharField(
        source='crop_listing.unit',
        read_only=True,
    )
    state = serializers.CharField(
        source='crop_listing.state',
        read_only=True,
    )
    district = serializers.CharField(
        source='crop_listing.district',
        read_only=True,
    )
    buyer_username = serializers.CharField(
        source='buyer.user.username',
        read_only=True,
    )
    farmer_username = serializers.CharField(
        source='crop_listing.farmer.user.username',
        read_only=True,
    )

    class Meta:
        model = Enquiry
        fields = [
            'id',
            'buyer_username',
            'farmer_username',
            'crop_listing',
            'crop_name',
            'listing_quantity',
            'listing_unit',
            'state',
            'district',
            'message',
            'requested_quantity',
            'farmer_response',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


class FarmerEnquiryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = ['farmer_response', 'status']
        read_only_fields = ['status']

    def validate_farmer_response(self, response):
        if not response.strip():
            raise serializers.ValidationError(
                'Farmer response cannot be empty.'
            )
        return response

    def validate(self, attrs):
        if self.instance.status != Enquiry.Status.OPEN:
            raise serializers.ValidationError(
                'Only open enquiries can receive a response.'
            )
        return attrs

    def update(self, instance, validated_data):
        instance.farmer_response = validated_data['farmer_response']
        instance.status = Enquiry.Status.RESPONDED
        instance.save()
        return instance


class OfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            'id',
            'enquiry',
            'offered_price',
            'quantity',
            'message',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def validate(self, attrs):
        enquiry = attrs['enquiry']
        offered_price = attrs['offered_price']
        quantity = attrs['quantity']

        buyer_profile = self.context['buyer_profile']
        listing = enquiry.crop_listing

        if enquiry.buyer_id != buyer_profile.id:
            raise serializers.ValidationError({
                'enquiry': 'You can only submit offers for your own enquiries.'
            })

        if listing.availability_status != CropListing.AvailabilityStatus.AVAILABLE:
            raise serializers.ValidationError({
                'enquiry': 'Offers cannot be submitted for unavailable listings.'
            })

        if enquiry.status in [
            Enquiry.Status.ACCEPTED,
            Enquiry.Status.REJECTED,
            Enquiry.Status.CLOSED,
        ]:
            raise serializers.ValidationError({
                'enquiry': 'This enquiry is no longer accepting offers.'
            })

        if offered_price <= Decimal('0'):
            raise serializers.ValidationError({
                'offered_price': 'Offered price must be greater than zero.'
            })

        if quantity <= Decimal('0'):
            raise serializers.ValidationError({
                'quantity': 'Offer quantity must be greater than zero.'
            })

        if quantity > enquiry.requested_quantity:
            raise serializers.ValidationError({
                'quantity': 'Offer quantity cannot exceed the requested quantity.'
            })

        if quantity > listing.quantity:
            raise serializers.ValidationError({
                'quantity': 'Offer quantity cannot exceed the listed quantity.'
            })

        return attrs


class OfferReadSerializer(serializers.ModelSerializer):
    crop_name = serializers.CharField(
        source='enquiry.crop_listing.crop.name',
        read_only=True,
    )
    buyer_username = serializers.CharField(
        source='enquiry.buyer.user.username',
        read_only=True,
    )
    farmer_username = serializers.CharField(
        source='enquiry.crop_listing.farmer.user.username',
        read_only=True,
    )
    crop_listing = serializers.IntegerField(
        source='enquiry.crop_listing_id',
        read_only=True,
    )
    enquiry_id = serializers.IntegerField(
        source='enquiry.id',
        read_only=True,
    )

    class Meta:
        model = Offer
        fields = [
            'id',
            'enquiry_id',
            'crop_listing',
            'crop_name',
            'buyer_username',
            'farmer_username',
            'offered_price',
            'quantity',
            'message',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


class FarmerOfferDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['status']

    def validate_status(self, status):
        if status not in [Offer.Status.ACCEPTED, Offer.Status.REJECTED]:
            raise serializers.ValidationError(
                'Farmer can only accept or reject an offer.'
            )

        if self.instance.status != Offer.Status.PENDING:
            raise serializers.ValidationError(
                'Only pending offers can be accepted or rejected.'
            )

        if (
            status == Offer.Status.ACCEPTED
            and self.instance.enquiry.crop_listing.availability_status
            != CropListing.AvailabilityStatus.AVAILABLE
        ):
            raise serializers.ValidationError(
                'An offer cannot be accepted for an unavailable listing.'
            )

        if status == Offer.Status.ACCEPTED:
            another_accepted = Offer.objects.filter(
                enquiry=self.instance.enquiry,
                status=Offer.Status.ACCEPTED,
            ).exclude(pk=self.instance.pk).exists()

            if another_accepted:
                raise serializers.ValidationError(
                    'Another offer for this enquiry has already been accepted.'
                )

        return status

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()

        if instance.status == Offer.Status.ACCEPTED:
            enquiry = instance.enquiry
            enquiry.status = Enquiry.Status.ACCEPTED
            enquiry.save(update_fields=['status', 'updated_at'])

        return instance
