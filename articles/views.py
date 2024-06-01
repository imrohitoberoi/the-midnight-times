from django.contrib.auth import get_user_model

from rest_framework import (
    generics as rest_generics,
    response as rest_response,
    status as rest_status,
    views as rest_views,
    viewsets as rest_viewsets,
)

from articles import (
    constants as articles_constants,
    models as articles_models,
    serializers as articles_serializers,
    utils as articles_utils,
)


class NewsArticleFetchView(rest_generics.CreateAPIView):
    queryset = articles_models.NewsArticle.objects.all()
    serializer_class = articles_serializers.NewsArticleFetchSerializer

    def create(self, request, *args, **kwargs):
        keyword = request.data.get('keyword')
        if not keyword:
            return rest_response.Response(
                { 'error': articles_constants.ERROR_MESSAGES['MISSING_KEYWORD'] },
                status=rest_status.HTTP_400_BAD_REQUEST
            )

        articles_data = articles_utils.fetch_news_articles(keyword)
        if articles_data is None:
            return rest_response.Response(
                { 'error': articles_constants.ERROR_MESSAGES['ERROR_FETCHING_ARTICLES'] },
                status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = self.serializer_class(data=articles_data, many=True)
        if serializer.is_valid():
            articles = self.serializer_class.save_articles(keyword, serializer.validated_data)
            # Retrieve the saved articles from the database using a unique identifier
            saved_articles = articles_models.NewsArticle.objects.filter(keyword=keyword)
            response_serializer = self.serializer_class(saved_articles, many=True)
            return rest_response.Response(response_serializer.data, status=rest_status.HTTP_201_CREATED)
        return rest_response.Response(serializer.errors, status=rest_status.HTTP_400_BAD_REQUEST)
