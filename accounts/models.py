from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    BaseUserManager,
    PermissionsMixin
)
from django.db import models

from accounts import constants as accounts_constants
from commons import models as common_models


class CustomUserManager(BaseUserManager):
    """
    CustomUser manager which checks for email and password validation
    """

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError(accounts_constants.ERROR_MESSAGES['MISSING_EMAIL'])
        user = self.model(
            email=self.normalize_email(email),
            created_at=datetime.now(),
            is_superuser=is_superuser,
            is_staff=is_staff,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class ActiveUsersManager(CustomUserManager):
    """
    This manager extends the `UserManager` to provide a queryset that filters out blocked users
    """
    def get_queryset(self):
        return super().get_queryset().exclude(status=self.model.BLOCKED)


class User(AbstractBaseUser, PermissionsMixin, common_models.BaseDateTimeModel):
    """
    Custom user model with base date time fields.
    """
    ACTIVE = 'active'
    BLOCKED = 'blocked'

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (BLOCKED, 'Blocked')
    )

    email = models.EmailField(unique=True, help_text=accounts_constants.HELP_TEXTS['EMAIL'])
    first_name = models.CharField(max_length=255, help_text=accounts_constants.HELP_TEXTS['FIRST_NAME'])
    last_name = models.CharField(
        max_length=255, null=True, blank=True, help_text=accounts_constants.HELP_TEXTS['LAST_NAME']
    )
    is_staff = models.BooleanField(default=False, help_text=accounts_constants.HELP_TEXTS['IS_STAFF'])
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default=ACTIVE, help_text=accounts_constants.HELP_TEXTS['STATUS']
    )
    keyword_quota = models.IntegerField(default=5, help_text=accounts_constants.HELP_TEXTS['KEYWORD_QUOTA'])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
    objects = ActiveUsersManager()
    all_objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """
        Property function to return full name of the user
        """
        return ' '.join(filter(None, [self.first_name, self.last_name]))
