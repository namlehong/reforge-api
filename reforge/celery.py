from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reforge.settings.dev')

app = Celery('reforge')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = 'redis://%s/0' % os.getenv('REDIS_HOST', '127.0.0.1:6379')
app.conf.result_backend = 'redis://%s/1' % os.getenv('REDIS_HOST', '127.0.0.1:6379')
app.conf.task_ignore_result = True

app.conf.timezone = 'Asia/Ho_Chi_Minh'

app.conf.CELERYBEAT_SCHEDULE = {
    'update-currency-5-mins': {
        'task': 'reforge.apps.poe.tasks.fix_hall',
        'schedule': crontab(minute='*/5'),
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
