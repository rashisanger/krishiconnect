from django.urls import path

from .views import (
    CropCatalogView,
    FarmerCropListingView,
    FarmerCropListingDetailView,
    BuyerAvailableCropListingView,
)

urlpatterns = [
    path('catalog/', CropCatalogView.as_view(), name='crop-catalog'),
    path('my-listings/', FarmerCropListingView.as_view(), name='farmer-crop-listings'),
    path('my-listings/<int:pk>/', FarmerCropListingDetailView.as_view(), name='farmer-crop-listing-detail'),
    path('available/', BuyerAvailableCropListingView.as_view(), name='available-crop-listings'),
]
