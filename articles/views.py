import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Count
from django.utils import timezone

from rest_framework import (
    exceptions as rest_exceptions,
    generics as rest_generics,
    response as rest_responses,
)

from articles import (
    constants as articles_constants,
    filters as articles_filters,
    models as articles_models,
    serializers as articles_serializers,
    utils as articles_utils,
)


class NewsArticleFetchView(rest_generics.ListAPIView):
    """
    View for fetching news articles.

    This view fetches news articles from the database and serializes them for display.
    It also supports filtering and ordering based on specified criteria.

    Attributes:
        queryset: The queryset containing all news articles.
        serializer_class: The serializer class used to serialize news articles.
        filterset_class: The filterset class used for filtering news articles.
        ordering: The default ordering of news articles (by published date, descending).
    """
    queryset = articles_models.NewsArticle.objects.all()
    serializer_class = articles_serializers.NewsArticleFetchSerializer
    filterset_class = articles_filters.NewsArticleFilter
    ordering = ['-published_at']

    def get_queryset(self, *args, **kwargs):
        keyword = self.request.query_params.get('keyword')
        if not keyword:
            raise rest_exceptions.ValidationError(articles_constants.ERROR_MESSAGES['MISSING_KEYWORD'])

        with transaction.atomic():
            last_search_time = self.check_quota_and_update_history(keyword, self.request.user)

            # If the time difference is less than the threshold, return without fetching articles
            if (
                last_search_time and timezone.localtime(timezone.now()) - last_search_time <
                datetime.timedelta(minutes=settings.THRESHOLD_ARTICLE_SEARCH_TIME_IN_MINUTES)
            ):
                latest_articles = []
            else:
                # Fetch updated articles for the provided keyword
                latest_articles = articles_utils.fetch_latest_news_articles(keyword)

            if isinstance(latest_articles, str):
                raise rest_exceptions.ValidationError(
                    f'{articles_constants.ERROR_MESSAGES["ERROR_FETCHING_ARTICLES"]}: {latest_articles}'
                )

            # Validate & save the articles fetched if needed
            if len(latest_articles) > 0:
                serializer = self.serializer_class(data=latest_articles, many=True)
                if serializer.is_valid():
                    self.serializer_class.save_articles(keyword, serializer.validated_data)

        return articles_models.NewsArticle.objects.filter(keyword=keyword)

    def check_quota_and_update_history(self, keyword, user):
        """
        Check user's keyword quota and update search history.

        This method checks if the user has reached their keyword quota. If the quota is not exceeded,
        it updates the search history with the provided keyword for the user.

        Args:
            keyword (str): The keyword to be checked and updated in the search history.
            user (User): The user for whom the keyword quota and search history are checked and updated.

        Returns:
            date: last search time of the keyword
        """
        # Get the user instance
        user_instance = get_user_model().objects.get(id=user.id)

        # Get or create the NewsArticleHistory object based on the keyword and user
        news_article_history, created = articles_models.NewsArticleHistory.objects.get_or_create(
            keyword=keyword, user=user
        )

        if created:
            # Check if the user's keyword quota is greater than zero
            if user_instance.keyword_quota > 0:
                # Decrease the user's keyword quota
                user_instance.keyword_quota -= 1
                user_instance.save(update_fields=['keyword_quota'])
                last_search_time = None
            else:
                # Delete the NewsArticleHistory object since it's not created
                news_article_history.delete()
                # Raise a validation error if the user's keyword quota is already zero
                raise rest_exceptions.ValidationError('Keyword quota exceeded. You cannot track more keywords.')
        else:
            last_search_time = articles_models.NewsArticleHistory.objects.filter(
                keyword=keyword
            ).latest('updated_at').updated_at
            # Update the updated_at field only
            news_article_history.save()
        return last_search_time


class NewsArticleHistoryListView(rest_generics.ListAPIView):
    """
    View for listing news article search history.

    This view lists the search history of news articles for the authenticated user.
    It returns a queryset filtered by the user and ordered by the latest update timestamp.

    Attributes:
        serializer_class: The serializer class used to serialize news article history.
        pagination_class: The pagination class (None to disable pagination).
    """
    serializer_class = articles_serializers.NewsArticleHistorySerializer
    pagination_class = None

    def get_queryset(self):
        return articles_models.NewsArticleHistory.objects.filter(user=self.request.user).order_by('-updated_at')


class MostSearchedKeywordsView(rest_generics.ListAPIView):
    """
    View for listing most searched keywords.

    This view lists the most searched keywords along with their search counts.
    It returns a queryset annotated with the count of distinct users searching for each keyword,
    ordered by the search count in descending order and limited to the top 5 keywords.

    Attributes:
        serializer_class: The serializer class used to serialize most searched keywords.
        pagination_class: The pagination class (None to disable pagination).
    """
    serializer_class = articles_serializers.MostSearchedKeywordsSerializer
    pagination_class = None

    def get_queryset(self):
        return articles_models.NewsArticleHistory.objects.values('keyword').annotate(
            count=Count('user', distinct=True)
        ).order_by('-count')[:5]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return rest_responses.Response(serializer.data)
