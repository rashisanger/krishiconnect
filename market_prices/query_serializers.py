
from rest_framework import serializers


class MarketPriceRefreshSerializer(serializers.Serializer):
    crop = serializers.CharField(required=False, max_length=100, allow_blank=False)
    state = serializers.CharField(required=False, max_length=100, allow_blank=False)
    district = serializers.CharField(required=False, max_length=100, allow_blank=False)
    mandi = serializers.CharField(required=False, max_length=150, allow_blank=False)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=100, default=100)


class MarketPriceFilterSerializer(serializers.Serializer):

    crop = serializers.CharField(
        required=False,
        allow_blank=False,
        max_length=100
    )

    state = serializers.CharField(
        required=False,
        allow_blank=False,
        max_length=100
    )

    district = serializers.CharField(
        required=False,
        allow_blank=False,
        max_length=100
    )

    mandi = serializers.CharField(
        required=False,
        allow_blank=False,
        max_length=150
    )

    date = serializers.DateField(
        required=False,
        input_formats=['%Y-%m-%d']
    )

    from_date = serializers.DateField(
        required=False,
        input_formats=['%Y-%m-%d']
    )

    to_date = serializers.DateField(
        required=False,
        input_formats=['%Y-%m-%d']
    )

    sort = serializers.ChoiceField(
        required=False,
        choices=[
            'modal_asc',
            'modal_desc',
            'date_asc',
            'date_desc'
        ]
    )

    def validate(self, attrs):

        from_date = attrs.get('from_date')
        to_date = attrs.get('to_date')

        if from_date and to_date and from_date > to_date:
            raise serializers.ValidationError({
                'to_date': 'to_date cannot be earlier than from_date.'
            })

        return attrs


class MarketPriceCompareQuerySerializer(
    MarketPriceFilterSerializer
):

    crop = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100
    )

    sort = serializers.ChoiceField(
        required=False,
        choices=['modal_asc', 'modal_desc'],
        default='modal_asc'
    )


class MarketPriceHistoryQuerySerializer(
    MarketPriceFilterSerializer
):

    crop = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100
    )

    mandi = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=150
    )
