# Generated by Django 5.0.6 on 2024-06-02 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_rename_publishedat_newsarticle_published_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsarticle',
            name='content',
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='author',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='description',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='source_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='source_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]