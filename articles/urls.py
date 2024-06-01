from django.urls import path

from articles import views as articles_views

urlpatterns = [
    path('news-articles-fetch/', articles_views.NewsArticleFetchView.as_view(), name='news-article-fetch'),
    # path('articles-history/', articles_views.ArticlesHistoryView.as_view(), name='articles-history'),
]
