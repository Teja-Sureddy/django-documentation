from celery import shared_task
import time
import redis
from my_project.settings import env


@shared_task(priority=255, retry_backoff=30, max_retries=5)
def my_background_task(*args, **kwargs):
    """
    routing_key:    priority
    retry_backoff:  delay between retries in seconds
    max_retries:    number of retry attempts
    """
    print(args, kwargs)
    for i in range(1, 6):
        print(i)
        time.sleep(1)


@shared_task
def push_to_redis(*args, **kwargs):
    print(args, kwargs)
    r = redis.Redis(
        host=env("REDIS_LOCATION").split(":")[1].replace("/", ""), decode_responses=True
    )

    r.set("key1", "value1")
    r.setex("key2", 5, "value2")  # expires in 5 secs
    r.mset({"key3": "value3", "key4": "value4"})


@shared_task
def pull_from_redis(*args, **kwargs):
    print(args, kwargs)
    r = redis.Redis(
        host=env("REDIS_LOCATION").split(":")[1].replace("/", ""), decode_responses=True
    )

    print("is_keys: ", r.exists("key1", "key2", "key3", "key4"))
    res = [r.get("key1"), r.get("key2"), r.mget("key3", "key4")]
    r.delete("key1", "key2", "key3", "key4")
    print("values: ", res)
