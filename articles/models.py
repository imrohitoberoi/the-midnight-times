from django.contrib.auth import get_user_model
from django.db import models

from articles import constants as article_constants
from commons import models as common_models


class NewsArticle(common_models.BaseDateTimeModel):
    keyword = models.CharField(null=True, max_length=article_constants.TEXT_FIELD_MAX_LENGTH)
    author = models.CharField(null=True, blank=True, max_length=article_constants.TEXT_FIELD_MAX_LENGTH)
    title = models.CharField(null=True, blank=True, max_length=article_constants.TEXT_FIELD_MAX_LENGTH)
    description = models.CharField(null=True, blank=True, max_length=article_constants.DESCRIPTION_FIELD_MAX_LENGTH)
    url = models.URLField(null=True, blank=True, max_length=article_constants.DESCRIPTION_FIELD_MAX_LENGTH)
    url_to_image = models.URLField(null=True, blank=True, max_length=article_constants.DESCRIPTION_FIELD_MAX_LENGTH)
    published_at = models.DateTimeField(null=True, blank=True)
    source_id = models.CharField(null=True, blank=True, max_length=article_constants.TEXT_FIELD_MAX_LENGTH)
    source_name = models.CharField(null=True, blank=True, max_length=article_constants.TEXT_FIELD_MAX_LENGTH)

    def __str__(self):
        return f'{self.keyword} - {self.title}'


class NewsArticleHistory(common_models.BaseDateTimeModel):
    keyword = models.CharField(max_length=article_constants.TEXT_FIELD_MAX_LENGTH)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email} - {self.keyword}'
