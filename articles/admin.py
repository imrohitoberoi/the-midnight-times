from django.contrib import admin

from articles import models as articles_models

# Registered articles model to be visible on django-admin UI
admin.site.register(articles_models.NewsArticle)
admin.site.register(articles_models.NewsArticleHistory)
