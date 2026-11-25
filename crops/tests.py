from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from farmers.models import FarmerProfile
from .models import Crop, CropListing


class FarmerListingSearchTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.farmer_user = user_model.objects.create_user(
            username='listing_farmer', email='listing_farmer@example.test',
            password='test-password', role='FARMER',
        )
        self.other_user = user_model.objects.create_user(
            username='other_farmer', email='other_farmer@example.test',
            password='test-password', role='FARMER',
        )
        self.farmer = FarmerProfile.objects.create(
            user=self.farmer_user, phone='+919876543210', address='Test farm',
            state='Maharashtra', district='Nashik',
        )
        self.other_farmer = FarmerProfile.objects.create(
            user=self.other_user, phone='+919876543211', address='Other farm',
            state='Maharashtra', district='Pune',
        )
        self.tomato, _ = Crop.objects.get_or_create(
            name='Tomato', defaults={'category': 'VEGETABLES'}
        )
        self.onion, _ = Crop.objects.get_or_create(
            name='Onion', defaults={'category': 'VEGETABLES'}
        )
        self.client.force_authenticate(self.farmer_user)

    def add_listing(self, farmer, crop):
        return CropListing.objects.create(
            farmer=farmer,
            crop=crop,
            quantity=Decimal('10'),
            unit='QUINTAL',
            expected_price=Decimal('1000'),
            state='Maharashtra',
            district='Nashik',
        )

    def test_farmer_search_filters_all_owned_listings_and_paginates_matches(self):
        for _ in range(6):
            self.add_listing(self.farmer, self.tomato)
        self.add_listing(self.farmer, self.onion)
        self.add_listing(self.other_farmer, self.tomato)

        first_page = self.client.get('/api/crops/my-listings/', {'search': 'toma', 'page': 1})
        second_page = self.client.get('/api/crops/my-listings/', {'search': 'toma', 'page': 2})

        self.assertEqual(first_page.status_code, 200)
        self.assertEqual(first_page.data['count'], 6)
        self.assertEqual(len(first_page.data['results']), 5)
        self.assertEqual(second_page.data['count'], 6)
        self.assertEqual(len(second_page.data['results']), 1)
        self.assertTrue(all(row['crop_name'] == 'Tomato' for row in first_page.data['results']))
