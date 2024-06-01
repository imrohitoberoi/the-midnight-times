from django.contrib import admin
from django.urls import include, path

api_urls = [
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
    path('commons/', include('commons.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]
