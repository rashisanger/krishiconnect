from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.test import APITestCase
from unittest.mock import Mock

from crops.models import Crop
from .models import MarketPrice
from .services import fetch_market_prices


class MarketPriceApiTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.admin = user_model.objects.create_user(
            username='market_admin', email='market_admin@example.test',
            password='test-password', role='ADMIN',
        )
        self.farmer = user_model.objects.create_user(
            username='market_farmer', email='market_farmer@example.test',
            password='test-password', role='FARMER',
        )
        self.crop = Crop.objects.create(name='Test Tomato', category='VEGETABLES')
        self.client.force_authenticate(self.admin)

    def add_price(self, *, district='Nashik', source='Market fixture', offset=0):
        return MarketPrice.objects.create(
            crop=self.crop,
            state='Maharashtra',
            district=district,
            mandi=f'Mandi {offset}',
            variety='Local',
            minimum_price=Decimal('1000'),
            modal_price=Decimal('1200'),
            maximum_price=Decimal('1400'),
            price_date=date.today() - timedelta(days=offset),
            source=source,
        )

    def test_location_filters_apply_and_source_is_reported_from_data(self):
        self.add_price(district='Nashik', source='KrishiConnect Demo')
        self.add_price(district='Pune', source='Agmarknet', offset=1)

        response = self.client.get('/api/market-prices/', {
            'state': 'Maharashtra', 'district': 'Nashik',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['source'], 'KrishiConnect Demo')
        self.assertEqual(response.data['results'][0]['district'], 'Nashik')

    def test_market_price_pagination_preserves_total_count(self):
        for offset in range(7):
            self.add_price(offset=offset)

        response = self.client.get('/api/market-prices/', {'page': 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 7)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIsNotNone(response.data['previous'])

    def test_mixed_sources_are_not_mislabeled_as_agmarknet(self):
        self.add_price(source='KrishiConnect Demo')
        self.add_price(source='Agmarknet', district='Nashik', offset=1)
        response = self.client.get('/api/market-prices/', {'state': 'Maharashtra'})
        self.assertEqual(response.data['source'], 'Multiple sources')

    def test_refresh_is_admin_only(self):
        self.client.force_authenticate(self.farmer)
        response = self.client.post('/api/market-prices/refresh/', {}, format='json')
        self.assertEqual(response.status_code, 403)

    @patch('market_prices.views.fetch_market_prices', return_value=[])
    def test_admin_can_refresh_without_writing_when_source_returns_no_records(self, fetch):
        response = self.client.post(
            '/api/market-prices/refresh/',
            {'state': 'Maharashtra', 'district': 'Nashik'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total_received'], 0)
        fetch.assert_called_once()


class AgmarknetFetchTests(TestCase):
    @override_settings(AGMARKNET_API_KEY='test-api-key')
    @patch('market_prices.services.requests.get')
    def test_fetch_passes_crop_and_location_filters(self, get):
        response = Mock()
        response.json.return_value = {'status': 'ok', 'records': []}
        get.return_value = response

        records = fetch_market_prices(
            limit=25,
            filters={
                'crop': 'Tomato',
                'state': 'Maharashtra',
                'district': 'Nashik',
                'mandi': 'Lasalgaon',
            },
        )

        params = get.call_args.kwargs['params']
        self.assertEqual(records, [])
        self.assertEqual(params['filters[commodity]'], 'Tomato')
        self.assertEqual(params['filters[state]'], 'Maharashtra')
        self.assertEqual(params['filters[district]'], 'Nashik')
        self.assertEqual(params['filters[market]'], 'Lasalgaon')
