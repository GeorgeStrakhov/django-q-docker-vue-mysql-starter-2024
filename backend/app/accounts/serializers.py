from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .models import MyUser as User

class UserRegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate_password(self, value):
        try:
            # Use Django's built-in password validators
            validate_password(value)
        except ValidationError as e:
            # Convert Django's password validation error to DRF's validation error
            raise serializers.ValidationError(list(e.messages))
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],  # Use email as username
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_verified:
            raise exceptions.PermissionDenied('User is not verified yet. Please check your email for the verification link.')
        if not user.is_active:
            raise exceptions.PermissionDenied('This user is marked as inactive. Please contact support.')

        # Add additional user data to the response payload
        data.update({
            'email': self.user.email,
            'payment_plan': self.user.payment_plan
        })

        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        try:
            # Decode the new access token to get the user ID
            access_token = RefreshToken(attrs['refresh']).access_token
            user_id = access_token['user_id']

            # Retrieve the user based on the ID
            user = User.objects.get(id=user_id)

            # Add additional user data to the response payload
            data.update({
                'email': user.email,
                'payment_plan': user.payment_plan  # Assuming the User model has a payment_plan attribute
            })
        except (TokenError, User.DoesNotExist) as e:
            raise InvalidToken('Invalid token or user does not exist')

        return data



