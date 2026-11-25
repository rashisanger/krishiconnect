
from django.urls import path

from .views import (
    BuyerProfileView,
    BuyerAvailableCropListingView,
    BuyerCropListingDetailView,
)


urlpatterns = [

    # View and update buyer profile
    path(
        'profile/',
        BuyerProfileView.as_view(),
        name='buyer-profile'
    ),

    # Browse and filter available farmer crop listings
    path(
        'listings/',
        BuyerAvailableCropListingView.as_view(),
        name='buyer-available-listings'
    ),

    # View individual available crop listing details
    path(
        'listings/<int:pk>/',
        BuyerCropListingDetailView.as_view(),
        name='buyer-listing-detail'
    ),

]
