from django.contrib.auth import get_user_model
from django.db import models

from articles import constants as article_constants
from commons import models as common_models


class NewsArticle(common_models.BaseDateTimeModel):
    """
    Model for storing news articles.
    Inherits from common_models.BaseDateTimeModel.
    """

    keyword = models.CharField(
        null=True,
        max_length=article_constants.TEXT_FIELD_MAX_LENGTH,
        help_text=article_constants.HELP_TEXTS['KEYWORD_ARTICLE']
    )
    author = models.CharField(
        null=True,
        blank=True,
        max_length=article_constants.TEXT_FIELD_MAX_LENGTH,
        help_text=article_constants.HELP_TEXTS['AUTHOR']
    )
    title = models.CharField(
        null=True,
        blank=True,
        max_length=article_constants.TEXT_FIELD_MAX_LENGTH,
        help_text=article_constants.HELP_TEXTS['TITLE']
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=article_constants.DESCRIPTION_FIELD_MAX_LENGTH,
        help_text=article_constants.HELP_TEXTS['DESCRIPTION']
    )
    url = models.URLField(
        null=True,
        blank=True,
        max_length=article_constants.DESCRIPTION_FIELD_MAX_LENGTH,
        help_text=article_constants.HELP_TEXTS['URL']
    )
    url_to_image = models.URLField(
        null=True,
        blank=True,
        max_length=article_constants.DESCRIPTION_FIELD_MAX_LENGTH,
        help_text=article_constants.HELP_TEXTS['URL_TO_IMAGE']
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=article_constants.HELP_TEXTS['PUBLISHED_AT']
    )
    source_id = models.CharField(
        null=True,
        blank=True,
        max_length=article_constants.TEXT_FIELD_MAX_LENGTH,
        help_text=article_constants.HELP_TEXTS['SOURCE_ID']
    )
    source_name = models.CharField(
        null=True,
        blank=True,
        max_length=article_constants.TEXT_FIELD_MAX_LENGTH,
        help_text=article_constants.HELP_TEXTS['SOURCE_NAME']
    )

    def __str__(self):
        """
        String representation of the object.
        Returns:
            str: Combination of keyword and title.
        """
        return f'{self.keyword} - {self.title}'


class NewsArticleHistory(common_models.BaseDateTimeModel):
    """
    Model for storing the history of news articles searched by users.
    """
    keyword = models.CharField(max_length=article_constants.TEXT_FIELD_MAX_LENGTH, help_text=article_constants.HELP_TEXTS['KEYWORD'])
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, help_text=article_constants.HELP_TEXTS['USER'])

    def __str__(self):
        """
        String representation of the object.
        Returns:
            str: User's email and the searched keyword.
        """
        return f'{self.user.email} - {self.keyword}'
