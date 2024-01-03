from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_bookstore.settings")

app = Celery("online_bookstore")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# To start
# celery -A your_project worker -l info
# celery -A your_project beat -l info
