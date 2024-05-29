from django.urls import path

from rest_framework import routers as rest_routers

from accounts import views as accounts_views

router = rest_routers.DefaultRouter()

router.register('users', accounts_views.AdminUserViewSet, basename='user')

urlpatterns = [
    path('login/', accounts_views.LoginView.as_view(), name='login'),
] + router.urls
