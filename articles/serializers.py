from datetime import datetime

from rest_framework import serializers

from articles import models as article_models

class NewsArticleFetchSerializer(serializers.ModelSerializer):
    class Meta:
        model = article_models.NewsArticle
        fields = '__all__'

    @staticmethod
    def save_articles(keyword, articles_data):
        articles_to_create = []
        for article_data in articles_data:
            source_id = None
            source_name = None
            if article_data.get('source'):
                source_id = article_data['source'].get('id')
                source_name = article_data['source'].get('name')
            # Creating news articles instances
            article = article_models.NewsArticle(
                keyword=keyword,
                author=article_data.get('author'),
                title=article_data.get('title'),
                description=article_data.get('description'),
                url=article_data.get('url'),
                urlToImage=article_data.get('urlToImage'),
                publishedAt=article_data.get('publishedAt'),
                content=article_data.get('content'),
                source_id=source_id,
                source_name=source_name
            )
            articles_to_create.append(article)

        # Bulk create news articles
        article_models.NewsArticle.objects.bulk_create(articles_to_create)
        return articles_to_create
