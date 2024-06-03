from rest_framework import serializers

from articles import models as article_models

class NewsArticleFetchSerializer(serializers.ModelSerializer):
    """
    Serializer for news articles fetched from an external API.
    """
    class Meta:
        model = article_models.NewsArticle
        fields = '__all__'

    @staticmethod
    def save_articles(keyword, articles_data):
        """
        Save news articles to the database.

        This function saves news articles to the database for a given keyword.

        Args:
            keyword (str): The keyword associated with the news articles.
            articles_data (list): A list of dictionaries containing data for each news article.

        Returns:
            None
        """
        articles_to_create = []
        for article_data in articles_data:
            source_id = None
            source_name = None
            if article_data.get('source'):
                source_id = article_data['source'].get('id')
                source_name = article_data['source'].get('name')

            # Creating news articles instances using provided data
            article = article_models.NewsArticle(
                keyword=keyword,
                author=article_data.get('author'),
                title=article_data.get('title'),
                description=article_data.get('description'),
                url=article_data.get('url'),
                url_to_image=article_data.get('urlToImage'),
                published_at=article_data.get('publishedAt'),
                source_id=source_id,
                source_name=source_name
            )
            articles_to_create.append(article)

        # Bulk create news articles
        article_models.NewsArticle.objects.bulk_create(articles_to_create)


class NewsArticleHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for news article history.
    """
    class Meta:
        model = article_models.NewsArticleHistory
        fields = '__all__'


class MostSearchedKeywordsSerializer(serializers.Serializer):
    """
    Serializer for the most searched keywords.
    """
    keyword = serializers.CharField()
    count = serializers.IntegerField()
