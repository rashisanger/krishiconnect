
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q


class Crop(models.Model):

    class Category(models.TextChoices):
        CEREALS = 'CEREALS', 'Cereals'
        PULSES = 'PULSES', 'Pulses'
        OILSEEDS = 'OILSEEDS', 'Oilseeds'
        VEGETABLES = 'VEGETABLES', 'Vegetables'
        FRUITS = 'FRUITS', 'Fruits'
        SPICES = 'SPICES', 'Spices'
        OTHER = 'OTHER', 'Other'

    name = models.CharField(
        max_length=100,
        unique=True
    )

    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CropListing(models.Model):

    class Unit(models.TextChoices):
        KG = 'KG', 'Kilogram'
        QUINTAL = 'QUINTAL', 'Quintal'
        TON = 'TON', 'Ton'

    class AvailabilityStatus(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        RESERVED = 'RESERVED', 'Reserved'
        SOLD = 'SOLD', 'Sold'
        INACTIVE = 'INACTIVE', 'Inactive'

    farmer = models.ForeignKey(
        'farmers.FarmerProfile',
        on_delete=models.CASCADE,
        related_name='crop_listings'
    )

    crop = models.ForeignKey(
        Crop,
        on_delete=models.PROTECT,
        related_name='listings'
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(0.001)]
    )

    unit = models.CharField(
        max_length=10,
        choices=Unit.choices,
        default=Unit.QUINTAL
    )

    expected_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    state = models.CharField(
        max_length=100
    )

    district = models.CharField(
        max_length=100
    )

    availability_status = models.CharField(
        max_length=15,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.AVAILABLE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gt=0),
                name='listing_quantity_positive'
            ),
            models.CheckConstraint(
                condition=Q(expected_price__gte=0),
                name='listing_price_nonnegative'
            )
        ]

    def __str__(self):
        return f"{self.crop.name} - {self.quantity} {self.unit}"
