from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from buyers.models import BuyerProfile
from crops.models import Crop, CropListing
from enquiries.models import Enquiry, Offer
from farmers.models import FarmerProfile
from market_prices.models import MarketPrice


DEMO_PASSWORD = 'KrishiDemo2026!'


class Command(BaseCommand):
    help = 'Create repeatable demo users, listings, market prices, enquiries and offers.'

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        now = timezone.now()

        farmer_user, created = User.objects.get_or_create(
            username='demo_farmer',
            defaults={
                'email': 'farmer.demo@krishiconnect.local',
                'first_name': 'Ravi',
                'last_name': 'Kumar',
                'role': User.Role.FARMER,
            },
        )
        if created:
            farmer_user.set_password(DEMO_PASSWORD)
            farmer_user.save(update_fields=['password'])
        FarmerProfile.objects.update_or_create(
            user=farmer_user,
            defaults={
                'phone': '+919876543210',
                'address': 'Demo Farm, Green Fields Road',
                'state': 'Maharashtra',
                'district': 'Nashik',
                'village': 'Deola',
                'pincode': '423102',
                'land_area': Decimal('8.50'),
                'land_area_unit': 'ACRE',
            },
        )

        buyer_user, created = User.objects.get_or_create(
            username='demo_buyer',
            defaults={
                'email': 'buyer.demo@krishiconnect.local',
                'first_name': 'Ananya',
                'last_name': 'Shah',
                'role': User.Role.BUYER,
            },
        )
        if created:
            buyer_user.set_password(DEMO_PASSWORD)
            buyer_user.save(update_fields=['password'])
        BuyerProfile.objects.update_or_create(
            user=buyer_user,
            defaults={
                'business_name': 'Harvest Basket Foods (Demo)',
                'phone': '+919876543211',
                'address': 'Market Road, Demo Trade Centre',
                'state': 'Maharashtra',
                'district': 'Pune',
                'buyer_type': BuyerProfile.BuyerType.WHOLESALER,
            },
        )

        crops = {}
        for name, category in [
            ('Demo Tomato', Crop.Category.VEGETABLES),
            ('Demo Onion', Crop.Category.VEGETABLES),
            ('Demo Wheat', Crop.Category.CEREALS),
            ('Demo Banana', Crop.Category.FRUITS),
        ]:
            crops[name], _ = Crop.objects.update_or_create(
                name=name,
                defaults={'category': category, 'description': 'Demonstration record for local preview.'},
            )

        listing_specs = [
            ('Demo Tomato', '18.000', 'QUINTAL', '2450.00', 'Nashik', 'Maharashtra'),
            ('Demo Onion', '32.000', 'QUINTAL', '1850.00', 'Nashik', 'Maharashtra'),
            ('Demo Wheat', '1200.000', 'KG', '28.50', 'Pune', 'Maharashtra'),
            ('Demo Banana', '4.000', 'TON', '31500.00', 'Jalgaon', 'Maharashtra'),
        ]
        listings = {}
        farmer_profile = FarmerProfile.objects.get(user=farmer_user)
        for name, quantity, unit, price, district, state in listing_specs:
            listings[name], _ = CropListing.objects.update_or_create(
                farmer=farmer_profile,
                crop=crops[name],
                defaults={
                    'quantity': Decimal(quantity),
                    'unit': unit,
                    'expected_price': Decimal(price),
                    'state': state,
                    'district': district,
                    'availability_status': CropListing.AvailabilityStatus.AVAILABLE,
                },
            )

        price_specs = [
            ('Demo Tomato', 'Nashik', 'Lasalgaon', 'Lasalgaon APMC', 'Local', '2100.00', '2800.00', '2450.00'),
            ('Demo Tomato', 'Pune', 'Pune', 'Pune Market Yard', 'Local', '2250.00', '2950.00', '2610.00'),
            ('Demo Onion', 'Nashik', 'Lasalgaon', 'Lasalgaon APMC', 'Red', '1600.00', '2200.00', '1875.00'),
            ('Demo Wheat', 'Pune', 'Pune', 'Pune Market Yard', 'Lokwan', '2600.00', '3100.00', '2840.00'),
            ('Demo Banana', 'Jalgaon', 'Jalgaon', 'Jalgaon APMC', 'Grand Naine', '2800.00', '3600.00', '3250.00'),
        ]
        price_date = date.today() - timedelta(days=1)
        for name, state, district, mandi, variety, minimum, maximum, modal in price_specs:
            MarketPrice.objects.update_or_create(
                crop=crops[name], state=state, district=district, mandi=mandi,
                variety=variety, price_date=price_date, source='KrishiConnect Demo',
                defaults={
                    'minimum_price': Decimal(minimum),
                    'maximum_price': Decimal(maximum),
                    'modal_price': Decimal(modal),
                },
            )

        buyer_profile = BuyerProfile.objects.get(user=buyer_user)
        enquiry, _ = Enquiry.objects.update_or_create(
            buyer=buyer_profile,
            crop_listing=listings['Demo Tomato'],
            defaults={
                'message': 'Hello Ravi, I’m interested in fresh tomatoes for our weekly market order. Could we discuss a pickup early next week?',
                'requested_quantity': Decimal('8.000'),
                'farmer_response': '',
                'status': Enquiry.Status.OPEN,
            },
        )
        Offer.objects.update_or_create(
            enquiry=enquiry,
            defaults={
                'offered_price': Decimal('2380.00'),
                'quantity': Decimal('5.000'),
                'message': 'We can collect from the farm and pay on pickup.',
                'status': Offer.Status.PENDING,
            },
        )

        # Add a resolved enquiry so the inbox shows a second conversation state.
        Enquiry.objects.update_or_create(
            buyer=buyer_profile,
            crop_listing=listings['Demo Onion'],
            defaults={
                'message': 'Would you have another small batch ready next week?',
                'requested_quantity': Decimal('10.000'),
                'farmer_response': 'Yes, another batch should be ready by Thursday. Please check back then.',
                'status': Enquiry.Status.RESPONDED,
            },
        )

        self.stdout.write(self.style.SUCCESS('Demo data is ready.'))
        self.stdout.write('Farmer login: demo_farmer / ' + DEMO_PASSWORD)
        self.stdout.write('Buyer login:  demo_buyer / ' + DEMO_PASSWORD)
        self.stdout.write(f'Crop listings: {CropListing.objects.filter(farmer=farmer_profile).count()}')
        self.stdout.write(f'Demo price records: {MarketPrice.objects.filter(source="KrishiConnect Demo").count()}')
        self.stdout.write(f'Demo enquiries: {Enquiry.objects.filter(buyer=buyer_profile).count()}')
        self.stdout.write(f'Demo offers: {Offer.objects.filter(enquiry__buyer=buyer_profile).count()}')
