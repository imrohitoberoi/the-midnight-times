from django.contrib import admin

from accounts import models as accounts_models

# Registered user model to be visible on django-admin UI
admin.site.register(accounts_models.User)
