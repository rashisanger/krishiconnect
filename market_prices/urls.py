
from django.urls import path

from .views import (
    MarketPriceListView,
    MarketPriceCompareView,
    MarketPriceHistoryView,
    MarketPriceRefreshView,
)


urlpatterns = [
    path(
        'refresh/',
        MarketPriceRefreshView.as_view(),
        name='market-price-refresh',
    ),
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
