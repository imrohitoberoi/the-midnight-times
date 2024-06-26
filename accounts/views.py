from django.contrib.auth import get_user_model

from rest_framework import (
    generics as rest_generics,
    response as rest_response,
    views as rest_views,
    viewsets as rest_viewsets,
)

from accounts import (
    constants as account_constants,
    permissions as account_permissions,
    serializers as account_serializers,
)
from commons import mixins as commons_mixins


class LoginView(rest_generics.CreateAPIView):
    """
    View for user login.
    Inherits from rest_framework.generics.CreateAPIView.
    """
    permission_classes = ()
    serializer_class = account_serializers.LoginSerializer


class LogoutView(rest_views.APIView):
    """
    View for user logout.
    Inherits from rest_framework.views.APIView.
    """
    def post(self, request):
        """
        POST method for user logout.
        Deletes the authentication token associated with the request.
        Returns a success message.
        """
        request.auth.delete()
        return rest_response.Response({'message': account_constants.SUCCESS_MESSAGES['LOGOUT']})


class AdminUserViewSet(commons_mixins.MultiSerializerClassViewSetMixin, rest_viewsets.ModelViewSet):
    """
    ViewSet for managing admin users.
    Inherits from rest_framework.viewsets.ModelViewSet.
    """
    serializer_classes = {
        'create': account_serializers.AdminUserRegistrationSerializer,
        'update': account_serializers.AdminUserDetailSerializer,
        'partial_update': account_serializers.AdminUserDetailSerializer,
        'list': account_serializers.AdminUserListSerializer,
        'retrieve': account_serializers.AdminUserDetailSerializer,
    }
    http_method_names = ['get', 'post', 'put', 'patch']
    queryset = get_user_model().all_objects.all()
    permission_classes = [account_permissions.IsAdminUser]
    pagination_class = None
