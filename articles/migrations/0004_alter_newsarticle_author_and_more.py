# Generated by Django 5.0.6 on 2024-06-03 02:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_remove_newsarticle_content_alter_newsarticle_author_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsarticle',
            name='author',
            field=models.CharField(blank=True, help_text='The author of the news article.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='description',
            field=models.CharField(blank=True, help_text='The description of the news article.', max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='keyword',
            field=models.CharField(help_text='The keyword associated with the news article.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='published_at',
            field=models.DateTimeField(blank=True, help_text='The datetime when the news article was published.', null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='source_id',
            field=models.CharField(blank=True, help_text='The ID of the source from which the news article originated.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='source_name',
            field=models.CharField(blank=True, help_text='The name of the source from which the news article originated.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='title',
            field=models.CharField(blank=True, help_text='The title of the news article.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='url',
            field=models.URLField(blank=True, help_text='The URL of the news article.', max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='url_to_image',
            field=models.URLField(blank=True, help_text='The URL to the image associated with the news article.', max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticlehistory',
            name='keyword',
            field=models.CharField(help_text='Keyword searched by the user.', max_length=255),
        ),
        migrations.AlterField(
            model_name='newsarticlehistory',
            name='user',
            field=models.ForeignKey(help_text='The user who searched for the news article.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
