import django_filters

from articles import models as articles_models


class NewsArticleFilter(django_filters.FilterSet):
    published_at = django_filters.DateFilter(field_name='published_at', lookup_expr='date')

    class Meta:
        model = articles_models.NewsArticle
        fields = ('published_at', 'source_id', 'source_name')
