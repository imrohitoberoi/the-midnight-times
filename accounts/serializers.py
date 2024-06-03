from django.contrib.auth import authenticate, get_user_model, password_validation

from rest_framework import (
    exceptions as rest_exceptions,
    serializers as rest_serializers,
)
from rest_framework.authtoken.models import Token

from accounts import constants as accounts_constants


class LoginSerializer(rest_serializers.Serializer):
    """
    Serializer used to validate the login credentials
    """

    email = rest_serializers.EmailField(max_length=accounts_constants.EMAIL_MAX_LENGTH, write_only=True)
    password = rest_serializers.CharField(max_length=accounts_constants.PASSWORD_MAX_LENGTH, write_only=True)
    token = rest_serializers.CharField(read_only=True)
    is_staff = rest_serializers.BooleanField(read_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        # Raise error for unauthenticated users
        if not user:
            raise rest_exceptions.AuthenticationFailed()

        # Handle case of blocked users
        if user.status == get_user_model().BLOCKED:
            raise rest_exceptions.ValidationError(accounts_constants.ERROR_MESSAGES['BLOCKED_USER'])

        data['user'] = user
        return data

    def create(self, validated_data):
        user_instance = validated_data['user']

        # Generate a token for the user.
        token, created = Token.objects.get_or_create(user=user_instance)
        validated_data['token'] = token.key
        validated_data['is_staff'] = user_instance.is_staff

        return validated_data


class AdminUserRegistrationSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for registering admin users.
    """
    password = rest_serializers.CharField(
        max_length=accounts_constants.PASSWORD_MAX_LENGTH,
        validators=[password_validation.validate_password],
        write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'last_name', 'keyword_quota']

    def create(self, validated_data):
        # Create user using 'create_user'
        return get_user_model().objects.create_user(**validated_data)


class AdminUserDetailSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for retrieving and updating admin user details
    """
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'keyword_quota', 'status', 'is_staff']


class AdminUserListSerializer(AdminUserDetailSerializer):
    """
    Serializer for listing admin users
    """
    class Meta(AdminUserDetailSerializer.Meta):
        fields = ['id', 'email', 'first_name', 'last_name', 'keyword_quota', 'status']
