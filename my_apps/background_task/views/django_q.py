from django.views import View
from django.http import JsonResponse
import time
from django_q.tasks import async_task


def my_background_task(*args, **kwargs):
    print(args, kwargs)
    for i in range(1, 6):
        print(i)
        time.sleep(1)


class DjangoQView(View):
    """
    Configuration:

    It runs the tasks in qcluster, `python manage.py qcluster` must be running.
    If the qcluster is down and then restarted, The pending tasks gets triggered automatically (stored in db).
    The number of simultaneous tasks that can be processed depends on the number of workers configured.
    """

    def post(self, request):
        """
        Running a task in the background.
        """
        async_task(my_background_task, 1, 2, x=3)
        return JsonResponse({"success": True}, status=200)
