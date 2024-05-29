from django.db import models


class BaseDateTimeModel(models.Model):
    """
    Abstract base class model that provides self-managed created_at and updated_at fields.
    """
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
