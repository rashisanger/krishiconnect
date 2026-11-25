
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/accounts/', include('accounts.urls')),
    path('api/farmers/', include('farmers.urls')),
    path('api/buyers/', include('buyers.urls')),
    path('api/crops/', include('crops.urls')),
    path('api/market-prices/', include('market_prices.urls')),
    path('api/enquiries/', include('enquiries.urls')),
    path('api/analytics/', include('analytics.urls')),
]
