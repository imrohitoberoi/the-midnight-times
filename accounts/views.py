from django.contrib.auth import get_user_model

from rest_framework import (
    generics as rest_generics,
    response as rest_response,
    views as rest_views,
    viewsets as rest_viewsets,
)

from accounts import (
    constants as account_constants,
    serializers as account_serializers
)
from commons import mixins as commons_mixins


class LoginView(rest_generics.CreateAPIView):
    permission_classes = ()
    serializer_class = account_serializers.LoginSerializer


class LogoutView(rest_views.APIView):
    permissions_required = []

    def post(self, request):
        request.auth.delete()
        return rest_response.Response({'message': account_constants.SUCCESS_MESSAGES['LOGOUT']})


class AdminUserViewSet(commons_mixins.MultiSerializerClassViewSetMixin, rest_viewsets.ModelViewSet):
    serializer_classes = {
        'create': account_serializers.AdminUserRegistrationSerializer,
        'update': account_serializers.AdminUserDetailSerializer,
        'partial_update': account_serializers.AdminUserDetailSerializer,
        'list': account_serializers.AdminUserListSerializer,
        'retrieve': account_serializers.AdminUserDetailSerializer,
    }
    http_method_names = ['get', 'post', 'put', 'patch']
    queryset = get_user_model().objects.all()
