from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r'^\+?[0-9]{10,15}$',
    message='Enter a valid phone number.'
)


class BuyerProfile(models.Model):

    class BuyerType(models.TextChoices):
        INDIVIDUAL = 'INDIVIDUAL', 'Individual'
        WHOLESALER = 'WHOLESALER', 'Wholesaler'
        RETAILER = 'RETAILER', 'Retailer'
        PROCESSOR = 'PROCESSOR', 'Processor'
        EXPORTER = 'EXPORTER', 'Exporter'
        OTHER = 'OTHER', 'Other'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='buyer_profile'
    )

    business_name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=16,
        validators=[phone_validator]
    )

    address = models.TextField()

    state = models.CharField(max_length=100)

    district = models.CharField(max_length=100)

    buyer_type = models.CharField(
        max_length=20,
        choices=BuyerType.choices
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.business_name} - {self.user.username}"