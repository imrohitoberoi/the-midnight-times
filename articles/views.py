from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import (
    exceptions as rest_exceptions,
    generics as rest_generics,
)

from articles import (
    constants as articles_constants,
    models as articles_models,
    serializers as articles_serializers,
    utils as articles_utils,
)


class NewsArticleFetchView(rest_generics.ListAPIView):
    queryset = articles_models.NewsArticle.objects.all()
    serializer_class = articles_serializers.NewsArticleFetchSerializer

    def get_queryset(self, *args, **kwargs):
        keyword = self.request.query_params.get('keyword')
        if not keyword:
            raise rest_exceptions.ValidationError(articles_constants.ERROR_MESSAGES['MISSING_KEYWORD'])

        with transaction.atomic():
            self.check_quota_and_update_history(keyword, self.request.user)

            # Fetch updated articles for the provided keyword
            latest_articles = articles_utils.fetch_latest_news_articles(keyword)
            if isinstance(latest_articles, str):
                raise rest_exceptions.ValidationError(
                    f'{articles_constants.ERROR_MESSAGES["ERROR_FETCHING_ARTICLES"]}: {latest_articles}'
                )

            # Save the articles fetched
            serializer = self.serializer_class(data=latest_articles, many=True)
            if serializer.is_valid():
                self.serializer_class.save_articles(keyword, serializer.validated_data)

            # Retrieve all articles from the database for the given keyword
            all_articles = articles_models.NewsArticle.objects.filter(keyword=keyword).order_by('published_at')
        return all_articles

    def check_quota_and_update_history(self, keyword, user):
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
            else:
                # Delete the NewsArticleHistory object since it's not created
                news_article_history.delete()
                # Raise a validation error if the user's keyword quota is already zero
                raise rest_exceptions.ValidationError('Keyword quota exceeded. You cannot track more keywords.')
        else:
            # Update the updated_at field only
            news_article_history.save()


class NewsArticleHistoryListView(rest_generics.ListAPIView):
    serializer_class = articles_serializers.NewsArticleHistorySerializer
    pagination_class = None

    def get_queryset(self):
        return articles_models.NewsArticleHistory.objects.filter(user=self.request.user)
