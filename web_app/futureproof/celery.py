from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futureproof.settings')

app = Celery('futureproof', broker='redis://redis:6379/0')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.task_create_missing_queues = True
app.conf.worker_prefetch_multiplier = 1

app.conf.update(worker_max_tasks_per_child=10)
app.conf.update(worker_max_memory_per_child=12000)
