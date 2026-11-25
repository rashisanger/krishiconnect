
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError

from accounts.permissions import IsBuyer
from .models import BuyerProfile

from crops.models import CropListing
from crops.pagination import CropListingPagination

from .serializers import (
    BuyerProfileSerializer,
    BuyerListingFilterSerializer,
    BuyerCropListingSerializer,
    BuyerCropListingDetailSerializer,
)


class BuyerProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = BuyerProfileSerializer

    permission_classes = [
        IsAuthenticated,
        IsBuyer,
    ]

    def get_object(self):

        try:
            return BuyerProfile.objects.select_related(
                'user'
            ).get(user=self.request.user)

        except BuyerProfile.DoesNotExist:
            raise NotFound('Buyer profile not found.')


class BuyerAvailableCropListingView(generics.ListAPIView):

    serializer_class = BuyerCropListingSerializer

    permission_classes = [
        IsAuthenticated,
        IsBuyer,
    ]

    pagination_class = CropListingPagination

    def get_queryset(self):

        allowed_parameters = set(
            BuyerListingFilterSerializer().fields.keys()
        ) | {'page', 'limit'}

        unknown_parameters = (
            set(self.request.query_params.keys())
            - allowed_parameters
        )

        if unknown_parameters:
            raise ValidationError({
                'query_params':
                    f'Unsupported filters: {", ".join(sorted(unknown_parameters))}'
            })

        filter_serializer = BuyerListingFilterSerializer(
            data=self.request.query_params
        )

        filter_serializer.is_valid(raise_exception=True)

        filters = filter_serializer.validated_data

        queryset = CropListing.objects.filter(
            availability_status=CropListing.AvailabilityStatus.AVAILABLE
        ).select_related(
            'crop',
            'farmer',
            'farmer__user'
        )

        if filters.get('crop'):
            queryset = queryset.filter(
                crop__name__icontains=filters['crop']
            )

        if filters.get('state'):
            queryset = queryset.filter(
                state__icontains=filters['state']
            )

        if filters.get('district'):
            queryset = queryset.filter(
                district__icontains=filters['district']
            )

        if filters.get('unit'):
            queryset = queryset.filter(
                unit=filters['unit']
            )

        if filters.get('min_quantity') is not None:
            queryset = queryset.filter(
                quantity__gte=filters['min_quantity']
            )

        if filters.get('max_quantity') is not None:
            queryset = queryset.filter(
                quantity__lte=filters['max_quantity']
            )

        if filters.get('min_expected_price') is not None:
            queryset = queryset.filter(
                expected_price__gte=filters['min_expected_price']
            )

        if filters.get('max_expected_price') is not None:
            queryset = queryset.filter(
                expected_price__lte=filters['max_expected_price']
            )

        return queryset.order_by('-created_at', '-id')


class BuyerCropListingDetailView(generics.RetrieveAPIView):

    serializer_class = BuyerCropListingDetailSerializer

    permission_classes = [
        IsAuthenticated,
        IsBuyer,
    ]

    lookup_field = 'pk'

    def get_queryset(self):

        return CropListing.objects.filter(
            availability_status=CropListing.AvailabilityStatus.AVAILABLE
        ).select_related(
            'crop',
            'farmer',
            'farmer__user'
        )
