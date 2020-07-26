from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.settings('DAJNGO_SETTINGS_MODULE', 'bookstore.settings')

app = Celery('bookstore')

app.config_from_object('django.comf:settings','CELERY')

app.autodiscover_tasks()
