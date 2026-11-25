from django.urls import path

from .views import (
    FarmerCropListingView,
    FarmerCropListingDetailView,
    BuyerAvailableCropListingView,
)

urlpatterns = [
    path('my-listings/', FarmerCropListingView.as_view(), name='farmer-crop-listings'),
    path('my-listings/<int:pk>/', FarmerCropListingDetailView.as_view(), name='farmer-crop-listing-detail'),
    path('available/', BuyerAvailableCropListingView.as_view(), name='available-crop-listings'),
]