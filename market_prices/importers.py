
from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.db import DatabaseError

from crops.models import Crop
from .models import MarketPrice


def import_market_price_records(records):
    """
    Validate and import Agmarknet records into the database.

    Existing records are updated instead of duplicated.
    Unknown commodities are added to the Crop table
    under the OTHER category.
    """

    created_count = 0
    updated_count = 0
    skipped_count = 0
    errors = []

    for index, record in enumerate(records, start=1):

        try:
            if not isinstance(record, dict):
                raise ValueError('Record is not a valid JSON object.')

            # Read and validate required text fields
            commodity = str(record.get('commodity', '')).strip()
            state = str(record.get('state', '')).strip()
            district = str(record.get('district', '')).strip()
            mandi = str(record.get('market', '')).strip()

            if not all([commodity, state, district, mandi]):
                raise ValueError('Missing commodity, state, district or market.')

            if len(commodity) > 100:
                raise ValueError('Commodity name exceeds 100 characters.')

            if len(state) > 100 or len(district) > 100:
                raise ValueError('State or district name exceeds 100 characters.')

            if len(mandi) > 150:
                raise ValueError('Market name exceeds 150 characters.')

            # Variety is optional
            variety = str(record.get('variety') or '').strip()

            if len(variety) > 100:
                raise ValueError('Variety name exceeds 100 characters.')

            # Parse arrival date: DD/MM/YYYY
            arrival_date = datetime.strptime(
                record.get('arrival_date', ''),
                '%d/%m/%Y'
            ).date()

            # Parse prices
            minimum_price = Decimal(str(record['min_price']))
            maximum_price = Decimal(str(record['max_price']))
            modal_price = Decimal(str(record['modal_price']))

            prices = [minimum_price, maximum_price, modal_price]

            if not all(price.is_finite() for price in prices):
                raise ValueError('Prices must be finite numbers.')

            if any(price < 0 for price in prices):
                raise ValueError('Prices cannot be negative.')

            if not (
                minimum_price <= modal_price <= maximum_price
            ):
                raise ValueError(
                    'Modal price must be between minimum and maximum prices.'
                )

            # Match an existing crop or create an uncategorized crop
            crop, _ = Crop.objects.get_or_create(
                name=commodity,
                defaults={
                    'category': Crop.Category.OTHER
                }
            )

            # Identify a unique market-price record
            lookup_fields = {
                'crop': crop,
                'state': state,
                'district': district,
                'mandi': mandi,
                'variety': variety,
                'price_date': arrival_date,
                'source': 'Agmarknet',
            }

            # Create a new record or update an existing one
            _, created = MarketPrice.objects.update_or_create(
                **lookup_fields,
                defaults={
                    'minimum_price': minimum_price,
                    'maximum_price': maximum_price,
                    'modal_price': modal_price,
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        except (
            ValueError,
            TypeError,
            KeyError,
            InvalidOperation,
            DatabaseError
        ) as exc:

            skipped_count += 1
            errors.append({
                'record': index,
                'error': str(exc)
            })

    return {
        'total_received': len(records),
        'created': created_count,
        'updated': updated_count,
        'skipped': skipped_count,
        'errors': errors,
    }
