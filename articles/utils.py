import requests

from django.conf import settings

from articles import constants as article_constants

def fetch_news_articles(keyword):
    try:
        url = (
            f"{article_constants.NEWS_API_URL}?q={keyword}&from=2024-05-01&sortBy=publishedAt&"
            f"apiKey={settings.NEWS_API_KEY}"
        )
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.json().get('articles', [])
    except Exception as e:
        return None
