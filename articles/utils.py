import json
import requests

from django.conf import settings
from django.db.models import Max

from articles import (
    constants as article_constants,
    models as article_models,
)

def fetch_latest_news_articles(keyword):
    try:
        # Check if there are any articles for the given keyword in the database
        latest_article_date = article_models.NewsArticle.objects.filter(
            keyword=keyword
        ).aggregate(Max('created_at'))['created_at__max']

        # If there are articles, use the latest created_at date as the from parameter
        if latest_article_date:
            from_date = latest_article_date.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            # If no articles found, use the default subscription date from settings
            from_date = settings.NEWS_API_SUBSCRIPTION_DATE

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
        return None
