from django.contrib.auth import get_user_model

from rest_framework import (
    generics as rest_generics,
    response as rest_response,
)

from commons import serializers as commons_serializers


class BaseDataView(rest_generics.GenericAPIView):
    serializer_class = commons_serializers.BaseDataSerializer

    def get(self, request, *args, **kwargs):
        return rest_response.Response(self.get_serializer(request.user).data)
