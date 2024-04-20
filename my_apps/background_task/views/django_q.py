from django.views import View
from django.http import JsonResponse
import time
from django_q.tasks import async_task, async_chain, schedule
from django.core.cache import cache


def my_background_task(*args, **kwargs):
    print(args, kwargs)
    for i in range(1, 6):
        print(i)
        time.sleep(1)

    value = cache.get("key1")
    print("value:", value)
    cache.delete("key1") if value else cache.set("key1", "value1")


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
        # the below runs concurrently
        async_task(my_background_task, 1, 2, x=3)
        async_task(my_background_task, 4, 5, x=6)

        # the below runs one after another (cache is used for sharing data)
        async_chain(
            [
                (my_background_task, [1, 2], {"x": 3}),
                (my_background_task, [4, 5], {"x": 6}),
            ]
        )

        # to schedule a task statically
        schedule(my_background_task, 1, 2, x=3, minutes=1)
        return JsonResponse({"success": True}, status=200)
