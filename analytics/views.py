
from django.db.models import Count, Avg, Q, Max
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from accounts.permissions import IsAdmin, IsFarmer
from farmers.models import FarmerProfile
from buyers.models import BuyerProfile
from crops.models import CropListing
from market_prices.models import MarketPrice
from enquiries.models import Enquiry, Offer

from .serializers import (
    CropAnalyticsQuerySerializer,
    MandiComparisonQuerySerializer,
)


def validate_query(serializer_class, query_params):
    serializer = serializer_class(data=query_params)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


def filter_market_prices(queryset, filters):
    if filters.get('crop'):
        queryset = queryset.filter(
            crop__name__icontains=filters['crop']
        )

    if filters.get('state'):
        queryset = queryset.filter(
            state__icontains=filters['state']
        )

    if filters.get('district'):
        queryset = queryset.filter(
            district__icontains=filters['district']
        )

    if filters.get('mandi'):
        queryset = queryset.filter(
            mandi__icontains=filters['mandi']
        )

    if filters.get('from_date'):
        queryset = queryset.filter(
            price_date__gte=filters['from_date']
        )

    if filters.get('to_date'):
        queryset = queryset.filter(
            price_date__lte=filters['to_date']
        )

    return queryset


class PlatformOverviewView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        available_listings = CropListing.objects.filter(
            availability_status=CropListing.AvailabilityStatus.AVAILABLE
        ).count()

        total_farmers = FarmerProfile.objects.count()
        total_buyers = BuyerProfile.objects.count()

        enquiry_stats = Enquiry.objects.aggregate(
            total=Count('id'),
            open=Count(
                'id',
                filter=Q(status=Enquiry.Status.OPEN),
            ),
            responded=Count(
                'id',
                filter=Q(status=Enquiry.Status.RESPONDED),
            ),
            accepted=Count(
                'id',
                filter=Q(status=Enquiry.Status.ACCEPTED),
            ),
            rejected=Count(
                'id',
                filter=Q(status=Enquiry.Status.REJECTED),
            ),
            closed=Count(
                'id',
                filter=Q(status=Enquiry.Status.CLOSED),
            ),
        )

        offer_stats = Offer.objects.aggregate(
            total=Count('id'),
            pending=Count(
                'id',
                filter=Q(status=Offer.Status.PENDING),
            ),
            accepted=Count(
                'id',
                filter=Q(status=Offer.Status.ACCEPTED),
            ),
            rejected=Count(
                'id',
                filter=Q(status=Offer.Status.REJECTED),
            ),
            withdrawn=Count(
                'id',
                filter=Q(status=Offer.Status.WITHDRAWN),
            ),
        )

        return Response({
            'total_available_crop_listings': available_listings,
            'total_registered_farmers': total_farmers,
            'total_registered_buyers': total_buyers,
            'enquiries': enquiry_stats,
            'offers': offer_stats,
        })


class CropAveragePriceView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filters = validate_query(
            CropAnalyticsQuerySerializer,
            request.query_params,
        )

        queryset = filter_market_prices(
            MarketPrice.objects.select_related('crop'),
            filters,
        )

        rows = queryset.values(
            'crop_id',
            'crop__name',
        ).annotate(
            average_modal_price=Avg('modal_price'),
            record_count=Count('id'),
        ).order_by('crop__name')

        labels = []
        values = []
        details = []

        for row in rows:
            average = row['average_modal_price']
            labels.append(row['crop__name'])
            values.append(float(average) if average is not None else None)
            details.append({
                'crop_id': row['crop_id'],
                'crop_name': row['crop__name'],
                'average_modal_price': (
                    float(average) if average is not None else None
                ),
                'record_count': row['record_count'],
            })

        return Response({
            'labels': labels,
            'datasets': [{
                'label': 'Average Modal Price',
                'data': values,
            }],
            'results': details,
        })


class HistoricalCropPriceView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filters = validate_query(
            CropAnalyticsQuerySerializer,
            request.query_params,
        )

        if not filters.get('crop'):
            return Response(
                {'crop': ['This query parameter is required.']},
                status=400,
            )

        queryset = filter_market_prices(
            MarketPrice.objects.select_related('crop'),
            filters,
        )

        rows = queryset.values(
            'price_date',
        ).annotate(
            average_modal_price=Avg('modal_price'),
            minimum_price=Avg('min_price'),
            maximum_price=Avg('max_price'),
            record_count=Count('id'),
        ).order_by('price_date')

        labels = []
        modal_prices = []
        minimum_prices = []
        maximum_prices = []
        results = []

        for row in rows:
            date_label = row['price_date'].isoformat()
            modal = row['average_modal_price']
            minimum = row['minimum_price']
            maximum = row['maximum_price']

            labels.append(date_label)
            modal_prices.append(
                float(modal) if modal is not None else None
            )
            minimum_prices.append(
                float(minimum) if minimum is not None else None
            )
            maximum_prices.append(
                float(maximum) if maximum is not None else None
            )

            results.append({
                'date': date_label,
                'average_modal_price': (
                    float(modal) if modal is not None else None
                ),
                'average_minimum_price': (
                    float(minimum) if minimum is not None else None
                ),
                'average_maximum_price': (
                    float(maximum) if maximum is not None else None
                ),
                'record_count': row['record_count'],
            })

        return Response({
            'labels': labels,
            'datasets': [
                {
                    'label': 'Average Modal Price',
                    'data': modal_prices,
                },
                {
                    'label': 'Average Minimum Price',
                    'data': minimum_prices,
                },
                {
                    'label': 'Average Maximum Price',
                    'data': maximum_prices,
                },
            ],
            'results': results,
        })


class MandiPriceComparisonView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filters = validate_query(
            MandiComparisonQuerySerializer,
            request.query_params,
        )

        queryset = MarketPrice.objects.filter(
            crop__name__iexact=filters['crop']
        )

        if filters.get('state'):
            queryset = queryset.filter(
                state__icontains=filters['state']
            )

        if filters.get('district'):
            queryset = queryset.filter(
                district__icontains=filters['district']
            )

        selected_date = filters.get('date')

        if selected_date:
            queryset = queryset.filter(price_date=selected_date)
        else:
            selected_date = queryset.aggregate(
                latest_date=Max('price_date')
            )['latest_date']

            if selected_date is None:
                return Response({
                    'crop': filters['crop'],
                    'date': None,
                    'labels': [],
                    'datasets': [{
                        'label': 'Average Modal Price',
                        'data': [],
                    }],
                    'results': [],
                })

            queryset = queryset.filter(price_date=selected_date)

        rows = queryset.values(
            'mandi',
            'state',
            'district',
        ).annotate(
            average_modal_price=Avg('modal_price'),
            minimum_price=Avg('min_price'),
            maximum_price=Avg('max_price'),
            record_count=Count('id'),
        ).order_by('average_modal_price')

        labels = []
        values = []
        results = []

        for row in rows:
            average = row['average_modal_price']
            labels.append(row['mandi'])
            values.append(
                float(average) if average is not None else None
            )

            results.append({
                'mandi': row['mandi'],
                'state': row['state'],
                'district': row['district'],
                'average_modal_price': (
                    float(average) if average is not None else None
                ),
                'average_minimum_price': (
                    float(row['minimum_price'])
                    if row['minimum_price'] is not None else None
                ),
                'average_maximum_price': (
                    float(row['maximum_price'])
                    if row['maximum_price'] is not None else None
                ),
                'record_count': row['record_count'],
            })

        return Response({
            'crop': filters['crop'],
            'date': selected_date.isoformat(),
            'labels': labels,
            'datasets': [{
                'label': 'Average Modal Price',
                'data': values,
            }],
            'results': results,
        })


class FarmerListingStatisticsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsFarmer]

    def get(self, request):
        try:
            farmer = FarmerProfile.objects.get(user=request.user)
        except FarmerProfile.DoesNotExist:
            raise NotFound('Farmer profile not found.')

        listing_stats = CropListing.objects.filter(
            farmer=farmer
        ).aggregate(
            total=Count('id'),
            available=Count(
                'id',
                filter=Q(
                    availability_status=CropListing.AvailabilityStatus.AVAILABLE
                ),
            ),
            reserved=Count(
                'id',
                filter=Q(
                    availability_status=CropListing.AvailabilityStatus.RESERVED
                ),
            ),
            sold=Count(
                'id',
                filter=Q(
                    availability_status=CropListing.AvailabilityStatus.SOLD
                ),
            ),
            inactive=Count(
                'id',
                filter=Q(
                    availability_status=CropListing.AvailabilityStatus.INACTIVE
                ),
            ),
        )

        crop_rows = CropListing.objects.filter(
            farmer=farmer
        ).values(
            'crop__name'
        ).annotate(
            listing_count=Count('id'),
            total_quantity=Count('quantity'),
        ).order_by('crop__name')

        return Response({
            'listing_statistics': listing_stats,
            'crop_wise_listings': [
                {
                    'crop_name': row['crop__name'],
                    'listing_count': row['listing_count'],
                }
                for row in crop_rows
            ],
            'chart': {
                'labels': [
                    row['crop__name'] for row in crop_rows
                ],
                'datasets': [{
                    'label': 'Crop Listings',
                    'data': [
                        row['listing_count'] for row in crop_rows
                    ],
                }],
            },
        })
