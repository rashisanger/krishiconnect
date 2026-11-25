
from django.urls import path

from .views import (
    BuyerEnquiryListCreateView,
    FarmerEnquiryListView,
    FarmerEnquiryResponseView,
    BuyerOfferListCreateView,
    FarmerOfferListView,
    FarmerOfferDecisionView,
)

urlpatterns = [
    # Buyer enquiries
    path(
        'buyer/',
        BuyerEnquiryListCreateView.as_view(),
        name='buyer-enquiries',
    ),

    # Farmer enquiries
    path(
        'farmer/',
        FarmerEnquiryListView.as_view(),
        name='farmer-enquiries',
    ),
    path(
        'farmer/<int:pk>/respond/',
        FarmerEnquiryResponseView.as_view(),
        name='farmer-enquiry-response',
    ),

    # Buyer offers
    path(
        'buyer/offers/',
        BuyerOfferListCreateView.as_view(),
        name='buyer-offers',
    ),

    # Farmer offers
    path(
        'farmer/offers/',
        FarmerOfferListView.as_view(),
        name='farmer-offers',
    ),
    path(
        'farmer/offers/<int:pk>/decision/',
        FarmerOfferDecisionView.as_view(),
        name='farmer-offer-decision',
    ),
]
