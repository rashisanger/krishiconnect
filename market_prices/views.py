
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.utils import timezone

from accounts.permissions import IsAdmin
from .services import fetch_market_prices, AgmarknetAPIError
from .importers import import_market_price_records

from .models import MarketPrice
from .serializers import MarketPriceSerializer
from .pagination import MarketPricePagination
from .query_serializers import (
    MarketPriceFilterSerializer,
    MarketPriceCompareQuerySerializer,
    MarketPriceHistoryQuerySerializer,
    MarketPriceRefreshSerializer,
)


def get_validated_filters(serializer_class, request):

    serializer = serializer_class(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    return serializer.validated_data


def filter_market_prices(filters):

    queryset = MarketPrice.objects.select_related('crop').all()

    if filters.get('crop'):
        queryset = queryset.filter(
            crop__name__icontains=filters['crop'].strip()
        )

    if filters.get('state'):
        queryset = queryset.filter(
            state__icontains=filters['state'].strip()
        )

    if filters.get('district'):
        queryset = queryset.filter(
            district__icontains=filters['district'].strip()
        )

    if filters.get('mandi'):
        queryset = queryset.filter(
            mandi__icontains=filters['mandi'].strip()
        )

    if filters.get('date'):
        queryset = queryset.filter(
            price_date=filters['date']
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


def apply_sorting(queryset, sort, default='date_desc'):

    sort = sort or default

    sorting_options = {
        'modal_asc': ['modal_price', 'mandi'],
        'modal_desc': ['-modal_price', 'mandi'],
        'date_asc': ['price_date', 'crop__name'],
        'date_desc': ['-price_date', 'crop__name'],
    }

    return queryset.order_by(*sorting_options[sort])


def paginated_chart_response(view, request, queryset, chart_type):

    paginator = MarketPricePagination()

    page = paginator.paginate_queryset(
        queryset,
        request,
        view=view
    )

    serializer = MarketPriceSerializer(page, many=True)

    results = serializer.data

    if chart_type == 'comparison':

        chart_data = {
            'labels': [
                item['mandi'] for item in results
            ],
            'minimum_prices': [
                float(item['minimum_price']) for item in results
            ],
            'maximum_prices': [
                float(item['maximum_price']) for item in results
            ],
            'modal_prices': [
                float(item['modal_price']) for item in results
            ],
        }

    else:

        chart_data = {
            'labels': [
                item['price_date'] for item in results
            ],
            'minimum_prices': [
                float(item['minimum_price']) for item in results
            ],
            'maximum_prices': [
                float(item['maximum_price']) for item in results
            ],
            'modal_prices': [
                float(item['modal_price']) for item in results
            ],
        }

    response = paginator.get_paginated_response(results)

    response.data['chart_data'] = chart_data

    return response


class MarketPriceListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        filters = get_validated_filters(
            MarketPriceFilterSerializer,
            request
        )

        queryset = filter_market_prices(filters)
        latest_price_date = queryset.order_by(
            '-price_date'
        ).values_list('price_date', flat=True).first()
        matching_count = queryset.count()
        sources = list(queryset.order_by().values_list('source', flat=True).distinct())

        queryset = apply_sorting(
            queryset,
            filters.get('sort')
        )

        paginator = MarketPricePagination()

        page = paginator.paginate_queryset(
            queryset,
            request,
            view=self
        )

        serializer = MarketPriceSerializer(
            page,
            many=True
        )

        response = paginator.get_paginated_response(serializer.data)
        response.data['count'] = matching_count
        response.data['latest_price_date'] = latest_price_date
        response.data['source'] = sources[0] if len(sources) == 1 else (
            'Multiple sources' if sources else None
        )
        return response


class MarketPriceRefreshView(APIView):
    """Fetch the latest matching Agmarknet records. Restricted to admins."""

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = MarketPriceRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filters = serializer.validated_data
        limit = filters.pop('limit', 100)

        try:
            records = fetch_market_prices(limit=limit, filters=filters)
        except AgmarknetAPIError as exc:
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        imported = import_market_price_records(records)
        return Response({
            'message': 'Agmarknet refresh completed.',
            'refreshed_at': timezone.now().isoformat(),
            'filters': filters,
            'total_received': imported['total_received'],
            'created': imported['created'],
            'updated': imported['updated'],
            'skipped': imported['skipped'],
            'errors': imported['errors'][:5],
        })


class MarketPriceCompareView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        filters = get_validated_filters(
            MarketPriceCompareQuerySerializer,
            request
        )

        queryset = filter_market_prices(filters)

        if filters.get('date'):
            selected_date = filters['date']

        else:
            selected_date = queryset.order_by(
                '-price_date'
            ).values_list(
                'price_date',
                flat=True
            ).first()

        if selected_date is None:

            return Response({
                'message': 'No market price data available for this crop and location.',
                'crop': filters['crop'],
                'price_date': None,
                'source': None,
                'count': 0,
                'results': [],
                'chart_data': {
                    'labels': [],
                    'minimum_prices': [],
                    'maximum_prices': [],
                    'modal_prices': [],
                },
            })

        queryset = queryset.filter(
            price_date=selected_date
        )

        queryset = apply_sorting(
            queryset,
            filters.get('sort'),
            default='modal_asc'
        )

        response = paginated_chart_response(
            self,
            request,
            queryset,
            'comparison'
        )

        response.data['crop'] = filters['crop']
        response.data['price_date'] = selected_date
        response.data['source'] = 'Agmarknet'

        response.data['interpretation'] = (
            'Modal prices are reported market prices, not guaranteed '
            'prices that an individual farmer will receive.'
        )

        return response


class MarketPriceHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        filters = get_validated_filters(
            MarketPriceHistoryQuerySerializer,
            request
        )

        queryset = filter_market_prices(filters)

        queryset = apply_sorting(
            queryset,
            filters.get('sort'),
            default='date_asc'
        )

        response = paginated_chart_response(
            self,
            request,
            queryset,
            'history'
        )

        response.data['crop'] = filters['crop']
        response.data['mandi'] = filters['mandi']

        response.data['message'] = (
            'Historical market prices retrieved successfully.'
            if response.data['count'] > 0
            else 'No historical price data available for this crop and mandi.'
        )

        return response
