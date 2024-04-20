from django.views import View
from django.http import JsonResponse
from my_apps.background_task.tasks import (
    my_background_task,
    push_to_redis,
    pull_from_redis,
)
from celery import chain


class CeleryView(View):
    """
    Configuration:

    Install redis on os and start redis-server by `sudo service redis-server start`.

    It runs the tasks in celery thread, `celery -A my_project worker -l info -P gevent` must be running.
    If the celery is down and then restarted, The pending tasks gets triggered automatically (django-celery-results).
    The number of simultaneous tasks that can be processed depends on the number of pools/workers configured.

    `-P gevent` is required for windows to run tasks concurrently.
    celery pools: prefork (default, doesnt work on windows), eventlet, gevent, solo.
    """

    def post(self, request):
        # Running a task in the background.
        my_background_task.delay(1, 2, x=3)

        share_data_between_tasks()
        return JsonResponse({"success": True}, status=200)


def share_data_between_tasks():
    """
    sharing data between two tasks using redis
    """
    # the below runs concurrently
    push_to_redis.delay(1, 2, x=3)
    pull_from_redis.delay(4, 5, x=6)

    # the below runs one after another
    chain(push_to_redis.s(1, 2, x=3), pull_from_redis.s(4, 5, x=6)).apply_async()
