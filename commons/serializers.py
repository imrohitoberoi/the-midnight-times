from django.contrib.auth import get_user_model

from rest_framework import serializers as rest_serializers


class BaseDataSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for serializing base data.
    """
    name = rest_serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'keyword_quota', 'is_staff']

    def get_name(self, obj):
        return obj.full_name
