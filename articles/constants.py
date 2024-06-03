TEXT_FIELD_MAX_LENGTH = 255
DESCRIPTION_FIELD_MAX_LENGTH = 2048

NEWS_API_URL = 'https://newsapi.org/v2/everything'

SUCCESS_MESSAGES = {
    'LOGOUT': 'Successfully logged out',
}

ERROR_MESSAGES = {
    'MISSING_KEYWORD': 'keyword is required in query param',
    'ERROR_FETCHING_ARTICLES': 'Failed to fetch articles',
}

HELP_TEXTS = {
    'KEYWORD': 'Keyword searched by the user.',
    'USER': 'The user who searched for the news article.',
    'KEYWORD_ARTICLE': 'The keyword associated with the news article.',
    'AUTHOR': 'The author of the news article.',
    'TITLE': 'The title of the news article.',
    'DESCRIPTION': 'The description of the news article.',
    'URL': 'The URL of the news article.',
    'URL_TO_IMAGE': 'The URL to the image associated with the news article.',
    'PUBLISHED_AT': 'The datetime when the news article was published.',
    'SOURCE_ID': 'The ID of the source from which the news article originated.',
    'SOURCE_NAME': 'The name of the source from which the news article originated.',
}
