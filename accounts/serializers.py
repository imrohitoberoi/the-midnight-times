from django.contrib.auth import authenticate, get_user_model, password_validation

from rest_framework import (
    exceptions as rest_exceptions,
    serializers as rest_serializers,
)
from rest_framework.authtoken.models import Token

from accounts import constants as accounts_constants


class LoginSerializer(rest_serializers.Serializer):
    """
    This Serializer class is used to validate the login credentials.
    """

    email = rest_serializers.EmailField(max_length=accounts_constants.EMAIL_MAX_LENGTH, write_only=True)
    password = rest_serializers.CharField(max_length=accounts_constants.PASSWORD_MAX_LENGTH, write_only=True)
    token = rest_serializers.CharField(read_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise rest_exceptions.AuthenticationFailed()

        if user.status == get_user_model().BLOCKED:
            raise rest_exceptions.ValidationError(accounts_constants.ERROR_MESSAGES['BLOCKED_USER'])

        data['user'] = user
        return data

    def create(self, validated_data):
        user_instance = validated_data['user']

        # Generate a token for the user.
        token = Token.objects.create(user=user_instance)
        validated_data['token'] = token.key
        return validated_data


class AdminUserRegistrationSerializer(rest_serializers.ModelSerializer):
    password = rest_serializers.CharField(
        max_length=accounts_constants.PASSWORD_MAX_LENGTH,
        validators=[password_validation.validate_password],
        write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'last_name', 'keyword_quota']


class AdminUserDetailSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'keyword_quota', 'status']


class AdminUserListSerializer(rest_serializers.ModelSerializer):
    name = rest_serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name', 'keyword_quota', 'status']

    def get_name(self, obj):
        return obj.full_name
