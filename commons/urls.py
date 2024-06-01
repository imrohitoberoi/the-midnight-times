from django.urls import path

from commons import views as commons_views

urlpatterns = [
    path('base-data/', commons_views.BaseDataView.as_view(), name='base-data'),
]
