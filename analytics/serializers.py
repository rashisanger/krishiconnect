
from rest_framework import serializers


class CropAnalyticsQuerySerializer(serializers.Serializer):
    crop = serializers.CharField(required=False, max_length=100)
    state = serializers.CharField(required=False, max_length=100)
    district = serializers.CharField(required=False, max_length=100)
    mandi = serializers.CharField(required=False, max_length=150)
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)

    def validate(self, attrs):
        from_date = attrs.get('from_date')
        to_date = attrs.get('to_date')

        if from_date and to_date and from_date > to_date:
            raise serializers.ValidationError({
                'to_date': 'End date cannot be earlier than start date.'
            })

        return attrs


class MandiComparisonQuerySerializer(serializers.Serializer):
    crop = serializers.CharField(required=True, max_length=100)
    state = serializers.CharField(required=False, max_length=100)
    district = serializers.CharField(required=False, max_length=100)
    date = serializers.DateField(required=False)
