
from rest_framework import generics, permissions

from accounts.permissions import IsFarmer, IsBuyer
from farmers.models import FarmerProfile

from .models import CropListing
from .serializers import CropListingSerializer
from .pagination import CropListingPagination


class FarmerCropListingView(generics.ListCreateAPIView):

    serializer_class = CropListingSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsFarmer
    ]

    pagination_class = CropListingPagination

    def get_queryset(self):
        return CropListing.objects.filter(
            farmer__user=self.request.user
        ).select_related('crop').order_by('-created_at')

    def perform_create(self, serializer):
        farmer_profile = FarmerProfile.objects.get(
            user=self.request.user
        )

        serializer.save(farmer=farmer_profile)


class FarmerCropListingDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = CropListingSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsFarmer
    ]

    def get_queryset(self):
        return CropListing.objects.filter(
            farmer__user=self.request.user
        ).select_related('crop')


class BuyerAvailableCropListingView(generics.ListAPIView):

    serializer_class = CropListingSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsBuyer
    ]

    pagination_class = CropListingPagination

    def get_queryset(self):
        queryset = CropListing.objects.filter(
            availability_status=CropListing.AvailabilityStatus.AVAILABLE
        ).select_related('crop').order_by('-created_at')

        crop_id = self.request.query_params.get('crop')
        state = self.request.query_params.get('state')
        district = self.request.query_params.get('district')
        unit = self.request.query_params.get('unit')

        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)

        if state:
            queryset = queryset.filter(state__icontains=state)

        if district:
            queryset = queryset.filter(district__icontains=district)

        if unit:
            queryset = queryset.filter(unit=unit.upper())

        return queryset
