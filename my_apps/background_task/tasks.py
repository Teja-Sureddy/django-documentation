from celery import shared_task
import time


@shared_task
def my_background_task(*args, **kwargs):
    print(args, kwargs)
    for i in range(1, 6):
        print(i)
        time.sleep(1)
