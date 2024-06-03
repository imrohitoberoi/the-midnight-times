import json
import requests
from datetime import datetime

from django.conf import settings
from django.db.models import Max

from articles import (
    constants as article_constants,
    models as article_models,
    serializers as article_serializers,
)
from themidnighttimes.celery import app


def fetch_latest_news_articles(keyword):
    """
    Fetch latest news articles for a given keyword.

    This function fetches the latest news articles related to the given keyword
    from an external API.

    Args:
        keyword (str): The keyword for which to fetch news articles.

    Returns:
        list: A list of dictionaries containing data for each news article.
    """
    try:
        # Check if there are any articles for the given keyword in the database
        latest_article_date = article_models.NewsArticle.objects.filter(
            keyword=keyword
        ).aggregate(Max('created_at'))['created_at__max']

        # If there are articles, use the latest created_at date as the 'from' query parameter
        if latest_article_date:
            from_date = latest_article_date.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            # If no articles found, use the first day of current month as free subscription plan of news api key
            # supports that only
            current_date = datetime.now()
            from_date = current_date.replace(day=1).date()

        all_articles = []
        page = 1

        while True:
            # Construct the URL with the appropriate page & from_date
            url = (
                f'{article_constants.NEWS_API_URL}?q={keyword}&from={from_date}'
                f'&sortBy=publishedAt&page={page}&apiKey={settings.NEWS_API_KEY}'
            )
            response = requests.get(url)
            if response.status_code != 200:
                try:
                    error_message = json.loads(response.text).get('message')
                except json.JSONDecodeError:
                    # If response is not in JSON format or does not contain 'message' field
                    # return the entire response text
                    error_message = response.text
                return error_message

            # Extract articles from the response
            articles_data = response.json().get('articles', [])
            all_articles.extend(articles_data)

            # Check if there are more pages to fetch
            total_results = response.json().get('totalResults', 0)
            if len(all_articles) == total_results or len(articles_data) == 0:
                # All articles have been fetched
                break

            # Increment page number for the next request
            page += 1

        return all_articles

    except Exception as e:
        return str(e)

@app.task
def refresh_searched_articles():
    """
    Task to refresh searched articles.

    This function fetches the unique keywords from the NewsArticleHistory model,
    and for each keyword, it fetches the latest news articles using fetch_latest_news_articles task.
    It then validates and saves the fetched articles.
    """
    # Fetching unique keywords from NewsArticleHistory model
    unique_keywords = article_models.NewsArticleHistory.objects.values_list('keyword', flat=True).distinct()

    for keyword in unique_keywords:
        # Fetching the latest articles for the keyword
        latest_articles = fetch_latest_news_articles(keyword)

        # Checking if fetched articles are valid and non-empty
        if isinstance(latest_articles, list) and len(latest_articles) > 0:
            serializer = article_serializers.NewsArticleFetchSerializer(data=latest_articles, many=True)
            if serializer.is_valid():
                # Saving the validated articles
                article_serializers.NewsArticleFetchSerializer.save_articles(keyword, serializer.validated_data)
