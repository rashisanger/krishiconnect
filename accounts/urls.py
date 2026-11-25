
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    FarmerRegistrationView,
    BuyerRegistrationView,
    LoginView,
    UserProfileView,
    LogoutView,
)

urlpatterns = [
    path('register/farmer/', FarmerRegistrationView.as_view(), name='farmer-register'),
    path('register/buyer/', BuyerRegistrationView.as_view(), name='buyer-register'),

    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
