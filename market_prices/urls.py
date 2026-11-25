
from django.urls import path

from .views import (
    MarketPriceListView,
    MarketPriceCompareView,
    MarketPriceHistoryView,
)


urlpatterns = [
    path(
        '',
        MarketPriceListView.as_view(),
        name='market-price-list'
    ),
    path(
        'compare/',
        MarketPriceCompareView.as_view(),
        name='market-price-compare'
    ),
    path(
        'history/',
        MarketPriceHistoryView.as_view(),
        name='market-price-history'
    ),
]
