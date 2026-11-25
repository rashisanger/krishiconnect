
from django.urls import path

from .views import (
    PlatformOverviewView,
    CropAveragePriceView,
    HistoricalCropPriceView,
    MandiPriceComparisonView,
    FarmerListingStatisticsView,
)

urlpatterns = [
    path(
        'overview/',
        PlatformOverviewView.as_view(),
        name='analytics-overview',
    ),
    path(
        'crop-average-prices/',
        CropAveragePriceView.as_view(),
        name='crop-average-prices',
    ),
    path(
        'historical-prices/',
        HistoricalCropPriceView.as_view(),
        name='historical-crop-prices',
    ),
    path(
        'mandi-comparison/',
        MandiPriceComparisonView.as_view(),
        name='mandi-price-comparison',
    ),
    path(
        'farmer/listing-statistics/',
        FarmerListingStatisticsView.as_view(),
        name='farmer-listing-statistics',
    ),
]
