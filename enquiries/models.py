
from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator

from buyers.models import BuyerProfile
from crops.models import CropListing


class Enquiry(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        RESPONDED = 'RESPONDED', 'Responded'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        CLOSED = 'CLOSED', 'Closed'

    buyer = models.ForeignKey(
        BuyerProfile,
        on_delete=models.CASCADE,
    )
    crop_listing = models.ForeignKey(
        CropListing,
        on_delete=models.PROTECT,
    )
    message = models.TextField()
    requested_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(0.001)],
    )
    farmer_response = models.TextField(blank=True, default='')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(requested_quantity__gt=0),
                name='enquiry_quantity_positive',
            ),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'Enquiry #{self.id} - {self.crop_listing.crop.name}'


class Offer(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        WITHDRAWN = 'WITHDRAWN', 'Withdrawn'

    enquiry = models.ForeignKey(
        Enquiry,
        on_delete=models.CASCADE,
    )
    offered_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(0.001)],
    )
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(offered_price__gte=0),
                name='offer_price_nonnegative',
            ),
            models.CheckConstraint(
                condition=Q(quantity__gt=0),
                name='offer_quantity_positive',
            ),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'Offer #{self.id} - Enquiry #{self.enquiry_id}'
