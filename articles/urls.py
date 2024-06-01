from django.urls import path

from articles import views as articles_views

urlpatterns = [
    path('news-article-fetch/', articles_views.NewsArticleFetchView.as_view(), name='news-article-fetch'),
    path('news-article-history/', articles_views.NewsArticleHistoryListView.as_view(), name='news-article-history'),
]
