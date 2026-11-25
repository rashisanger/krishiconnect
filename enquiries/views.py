
from django.db import transaction
from rest_framework import generics
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsBuyer, IsFarmer
from buyers.models import BuyerProfile
from farmers.models import FarmerProfile
from crops.pagination import CropListingPagination

from .models import Enquiry, Offer
from .serializers import (
    EnquiryCreateSerializer,
    EnquiryReadSerializer,
    FarmerEnquiryResponseSerializer,
    OfferCreateSerializer,
    OfferReadSerializer,
    FarmerOfferDecisionSerializer,
)


def get_buyer_profile(user):
    try:
        return BuyerProfile.objects.get(user=user)
    except BuyerProfile.DoesNotExist:
        raise NotFound('Buyer profile not found.')


def get_farmer_profile(user):
    try:
        return FarmerProfile.objects.get(user=user)
    except FarmerProfile.DoesNotExist:
        raise NotFound('Farmer profile not found.')


class BuyerEnquiryListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsBuyer]
    pagination_class = CropListingPagination

    def get_queryset(self):
        buyer = get_buyer_profile(self.request.user)
        return Enquiry.objects.filter(
            buyer=buyer
        ).select_related(
            'buyer__user',
            'crop_listing__crop',
            'crop_listing__farmer__user',
        ).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EnquiryCreateSerializer
        return EnquiryReadSerializer

    def perform_create(self, serializer):
        buyer = get_buyer_profile(self.request.user)
        serializer.save(buyer=buyer)


class FarmerEnquiryListView(generics.ListAPIView):
    serializer_class = EnquiryReadSerializer
    permission_classes = [IsAuthenticated, IsFarmer]
    pagination_class = CropListingPagination

    def get_queryset(self):
        farmer = get_farmer_profile(self.request.user)

        return Enquiry.objects.filter(
            crop_listing__farmer=farmer
        ).select_related(
            'buyer__user',
            'crop_listing__crop',
            'crop_listing__farmer__user',
        ).order_by('-created_at')


class FarmerEnquiryResponseView(generics.UpdateAPIView):
    serializer_class = FarmerEnquiryResponseSerializer
    permission_classes = [IsAuthenticated, IsFarmer]
    http_method_names = ['patch', 'options', 'head']

    def get_queryset(self):
        farmer = get_farmer_profile(self.request.user)
        return Enquiry.objects.filter(
            crop_listing__farmer=farmer
        )

    def perform_update(self, serializer):
        serializer.save()


class BuyerOfferListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsBuyer]
    pagination_class = CropListingPagination

    def get_queryset(self):
        buyer = get_buyer_profile(self.request.user)

        return Offer.objects.filter(
            enquiry__buyer=buyer
        ).select_related(
            'enquiry__buyer__user',
            'enquiry__crop_listing__crop',
            'enquiry__crop_listing__farmer__user',
        ).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferReadSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['buyer_profile'] = get_buyer_profile(self.request.user)
        return context


class FarmerOfferListView(generics.ListAPIView):
    serializer_class = OfferReadSerializer
    permission_classes = [IsAuthenticated, IsFarmer]
    pagination_class = CropListingPagination

    def get_queryset(self):
        farmer = get_farmer_profile(self.request.user)

        return Offer.objects.filter(
            enquiry__crop_listing__farmer=farmer
        ).select_related(
            'enquiry__buyer__user',
            'enquiry__crop_listing__crop',
            'enquiry__crop_listing__farmer__user',
        ).order_by('-created_at')


class FarmerOfferDecisionView(generics.UpdateAPIView):
    serializer_class = FarmerOfferDecisionSerializer
    permission_classes = [IsAuthenticated, IsFarmer]
    http_method_names = ['patch', 'options', 'head']

    def get_queryset(self):
        farmer = get_farmer_profile(self.request.user)

        return Offer.objects.filter(
            enquiry__crop_listing__farmer=farmer
        ).select_related(
            'enquiry__crop_listing'
        )

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save()
