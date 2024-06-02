from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'themidnighttimes_schedule_task': {
        'task': 'articles.utils.refresh_searched_articles',
        'schedule': crontab(minute=0, hour='*/1'), # Run every hour
        'description': 'Fetch latest news articles every 1 hour',
    },
}
