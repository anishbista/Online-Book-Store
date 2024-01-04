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

"""Celery Worker: Running the worker process is essential if you have tasks that need to be executed asynchronously. Workers are responsible for picking up tasks from the queue and processing them. If your application uses Celery to handle background or asynchronous tasks, you'll need at least one worker process running.

Celery Beat: The beat process is used to schedule and execute periodic tasks. If your application has tasks that need to run on a regular schedule (like hourly, daily, etc.), then the beat process is necessary. It's like a scheduler that triggers these tasks at specified intervals.

In many cases, you might need both the worker and beat processes running simultaneously to handle both immediate asynchronous tasks and scheduled periodic tasks.

If your application doesn't have any periodic tasks or doesn't require scheduling, you might not need to run the beat process. However, if you have asynchronous tasks, the worker process is essential for their execution.

For instance, if your application has asynchronous tasks but no scheduled periodic tasks, you'd only need to run the worker process. If you have scheduled tasks but no asynchronous tasks, you'd only need to run the beat process. If you have both, then you'd need to run both processes concurrently.






"""
