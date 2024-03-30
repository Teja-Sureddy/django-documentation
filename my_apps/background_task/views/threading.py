from django.views import View
from threading import Thread
from django.http import JsonResponse
import time


class MyBackgroundThreadingTask(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        This method runs in the background.
        """
        print(self.args, self.kwargs)
        for i in range(1, 6):
            print(i)
            time.sleep(1)


class ThreadingView(View):
    def post(self, request):
        task_thread = MyBackgroundThreadingTask()
        task_thread.start()
        return JsonResponse({'success': True}, status=200)
