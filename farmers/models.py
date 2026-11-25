from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator


phone_validator = RegexValidator(
    regex=r'^\+?[0-9]{10,15}$',
    message='Enter a valid phone number.'
)


class FarmerProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='farmer_profile'
    )

    phone = models.CharField(
        max_length=16,
        validators=[phone_validator]
    )

    address = models.TextField()

    state = models.CharField(max_length=100)

    district = models.CharField(max_length=100)

    village = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    land_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )

    land_area_unit = models.CharField(
        max_length=20,
        default='ACRE'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Farmer: {self.user.username}"