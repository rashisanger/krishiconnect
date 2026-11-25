from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from crops.models import Crop
from market_prices.models import MarketPrice


class PlatformOverviewAnalyticsTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.admin = user_model.objects.create_user(
            username='analytics_admin', email='analytics_admin@example.test',
            password='test-password', role='ADMIN',
        )
        self.farmer = user_model.objects.create_user(
            username='analytics_farmer', email='analytics_farmer@example.test',
            password='test-password', role='FARMER',
        )
        self.crop = Crop.objects.create(name='Analytics Tomato', category='VEGETABLES')
        MarketPrice.objects.create(
            crop=self.crop,
            state='Maharashtra',
            district='Nashik',
            mandi='Lasalgaon',
            variety='Local',
            minimum_price=Decimal('1000'),
            modal_price=Decimal('1200'),
            maximum_price=Decimal('1400'),
            price_date=date.today(),
            source='Analytics fixture',
        )

    def test_overview_includes_listing_breakdown_and_price_trend_for_admin(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get('/api/analytics/overview/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['listings'], {
            'total': 0, 'available': 0, 'reserved': 0, 'sold': 0, 'inactive': 0,
        })
        self.assertEqual(response.data['market_price_trend'][0]['record_count'], 1)
        self.assertEqual(response.data['market_price_trend'][0]['average_modal_price'], 1200.0)

    def test_overview_is_not_available_to_non_admin(self):
        self.client.force_authenticate(self.farmer)
        response = self.client.get('/api/analytics/overview/')
        self.assertEqual(response.status_code, 403)
