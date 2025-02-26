import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Create the Celery app
app = Celery('backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'send-daily-weather-stats': {
        'task': 'weather.tasks.send_daily_stats_email',
        # 'schedule': crontab(hour=23, minute=59),  # Run at 9:00 AM every day
        'schedule': crontab(minute='*/1'), # Run every minute
    },
}