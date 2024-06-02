import os
import celery

from django.conf import settings

from themidnighttimes import schedules as themidnighttimes_schedules

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'themidnighttimes.settings')

app = celery.Celery('themidnighttimes')

# Configure Celery app settings
app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    accept_content=settings.CELERY_ACCEPT_CONTENT,
    beat_scheduler=settings.CELERY_BEAT_SCHEDULER,
)

# Define the beat schedule
app.conf.beat_schedule = themidnighttimes_schedules.CELERY_BEAT_SCHEDULE

# Autodiscover and register all async tasks from all installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
