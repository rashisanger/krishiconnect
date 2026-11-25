
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsFarmer
from .models import FarmerProfile
from .serializers import FarmerProfileSerializer


class FarmerProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = FarmerProfileSerializer

    permission_classes = [
        IsAuthenticated,
        IsFarmer
    ]

    def get_object(self):
        return FarmerProfile.objects.get(user=self.request.user)
