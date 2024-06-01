from django.contrib import admin

from articles import models as articles_models

admin.site.register(articles_models.NewsArticle)
admin.site.register(articles_models.NewsArticleHistory)
