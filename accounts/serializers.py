
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from farmers.models import FarmerProfile
from buyers.models import BuyerProfile


User = get_user_model()


class FarmerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    phone = serializers.CharField(max_length=16)
    address = serializers.CharField()
    state = serializers.CharField(max_length=100)
    district = serializers.CharField(max_length=100)
    village = serializers.CharField(max_length=100, required=False, allow_blank=True)
    pincode = serializers.CharField(max_length=10, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name',
            'phone', 'address', 'state', 'district',
            'village', 'pincode'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password2': 'Passwords do not match.'
            })
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'This email is already registered.'
            )
        return value

    def create(self, validated_data):
        validated_data.pop('password2')

        profile_data = {
            'phone': validated_data.pop('phone'),
            'address': validated_data.pop('address'),
            'state': validated_data.pop('state'),
            'district': validated_data.pop('district'),
            'village': validated_data.pop('village', ''),
            'pincode': validated_data.pop('pincode', ''),
        }

        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password,
            role=User.Role.FARMER,
            **validated_data
        )

        FarmerProfile.objects.create(user=user, **profile_data)

        return user


class BuyerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    business_name = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=16)
    address = serializers.CharField()
    state = serializers.CharField(max_length=100)
    district = serializers.CharField(max_length=100)
    buyer_type = serializers.ChoiceField(
        choices=BuyerProfile.BuyerType.choices
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name',
            'business_name', 'phone', 'address',
            'state', 'district', 'buyer_type'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password2': 'Passwords do not match.'
            })
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'This email is already registered.'
            )
        return value

    def create(self, validated_data):
        validated_data.pop('password2')

        profile_data = {
            'business_name': validated_data.pop('business_name'),
            'phone': validated_data.pop('phone'),
            'address': validated_data.pop('address'),
            'state': validated_data.pop('state'),
            'district': validated_data.pop('district'),
            'buyer_type': validated_data.pop('buyer_type'),
        }

        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password,
            role=User.Role.BUYER,
            **validated_data
        )

        BuyerProfile.objects.create(user=user, **profile_data)

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    farmer_profile = serializers.SerializerMethodField()
    buyer_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'farmer_profile',
            'buyer_profile'
        ]

    def get_farmer_profile(self, obj):
        try:
            profile = obj.farmer_profile
        except FarmerProfile.DoesNotExist:
            return None

        return {
            'phone': profile.phone,
            'address': profile.address,
            'state': profile.state,
            'district': profile.district,
            'village': profile.village,
            'pincode': profile.pincode,
        }

    def get_buyer_profile(self, obj):
        try:
            profile = obj.buyer_profile
        except BuyerProfile.DoesNotExist:
            return None

        return {
            'business_name': profile.business_name,
            'phone': profile.phone,
            'address': profile.address,
            'state': profile.state,
            'district': profile.district,
            'buyer_type': profile.buyer_type,
        }
