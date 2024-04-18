from django.views import View
from django.http import JsonResponse
from my_apps.background_task.tasks import my_background_task


class CeleryView(View):
    """
    celery

    Configure celery in django.
    Install redis in os and start redis-server by `sudo service redis-server start`.

    It runs the tasks in celery thread, `celery -A my_project worker -l info -P gevent` must be running.
    If the celery is down and then restarted, The pending tasks gets triggered automatically (django-celery-results).
    The number of simultaneous tasks that can be processed depends on the number of pools/workers configured.

    `-P gevent` is required for windows to run tasks concurrently.
    celery pools: prefork (default, doesnt work on windows), eventlet, gevent, solo.
    """

    def post(self, request):
        """
        Running a task in the background (can run multiple simultaneously).
        """
        my_background_task.delay(1, 2, x=3)
        return JsonResponse({"success": True}, status=200)
