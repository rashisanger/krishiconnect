
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def home(request):
    """Provide a helpful response when the server root is opened in a browser."""
    return JsonResponse({
        'name': 'KrishiConnect API',
        'api': '/api/',
        'admin': '/admin/',
    })


def api_index(request):
    """List the available API modules."""
    return JsonResponse({
        'accounts': '/api/accounts/',
        'farmers': '/api/farmers/',
        'buyers': '/api/buyers/',
        'crops': '/api/crops/',
        'market_prices': '/api/market-prices/',
        'enquiries': '/api/enquiries/',
        'analytics': '/api/analytics/',
    })


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', api_index, name='api-index'),

    path('api/accounts/', include('accounts.urls')),
    path('api/farmers/', include('farmers.urls')),
    path('api/buyers/', include('buyers.urls')),
    path('api/crops/', include('crops.urls')),
    path('api/market-prices/', include('market_prices.urls')),
    path('api/enquiries/', include('enquiries.urls')),
    path('api/analytics/', include('analytics.urls')),
]
