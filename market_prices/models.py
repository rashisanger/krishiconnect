from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q, F


class MarketPrice(models.Model):

    crop = models.ForeignKey(
        'crops.Crop',
        on_delete=models.PROTECT,
        related_name='market_prices'
    )

    state = models.CharField(max_length=100)

    district = models.CharField(max_length=100)

    mandi = models.CharField(max_length=150)

    variety = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    minimum_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    maximum_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    modal_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    price_date = models.DateField()

    source = models.CharField(
        max_length=100,
        default='Agmarknet'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(minimum_price__lte=F('maximum_price')),
                name='market_min_lte_max'
            ),
            models.CheckConstraint(
                condition=(
                    Q(modal_price__gte=F('minimum_price')) &
                    Q(modal_price__lte=F('maximum_price'))
                ),
                name='market_modal_between_prices'
            ),
            models.UniqueConstraint(
                fields=[
                    'crop',
                    'state',
                    'district',
                    'mandi',
                    'variety',
                    'price_date',
                    'source'
                ],
                name='unique_market_price_record'
            )
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        super().clean()

        if (
            self.minimum_price is not None
            and self.maximum_price is not None
            and self.modal_price is not None
        ):
            if not (
                self.minimum_price <= self.modal_price
                <= self.maximum_price
            ):
                raise ValidationError(
                    'Modal price must be between minimum and maximum prices.'
                )

    def __str__(self):
        return f"{self.crop.name} - {self.mandi} - {self.price_date}"