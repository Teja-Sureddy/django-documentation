# Background Tasks

---
## Inbuilt

### threading

 - Concurrent task execution (background & foreground).
 - Can access and modify shared data between tasks.
 - Good for I/O-bound tasks but not for CPU-bound tasks due to GIL.
 - It shares common memory space.

### multiprocessing

 - Concurrent task execution (background & foreground).
 - Can access and modify shared data between tasks using shared memory, queues or pipes.
 - Good for CPU-bound tasks as it can utilize multiple CPUs.
 - Each process has its own memory space.

---
## 3rd Party

### apscheduler

 - Scheduled tasks (CRON, Interval, ...).
 - Good for I/O-bound tasks but not for CPU-bound tasks due to single-threaded nature.
 - Has management - Can add, modify, and remove scheduled tasks dynamically.
 - It supports both sync and async job execution.

### celery

 - Concurrent task execution (background & foreground).
 - Can access and modify shared data between tasks using `redis`, rabbitmq, cache or database.
 - Good for both I/O-bound and CPU-bound tasks.
 - Can have Scheduled tasks (CRON) statically using celery itself, dynamically using `django-celery-beat`.
 - Has monitoring and management using `flower`, retry mechanism and prioritization.
 - Can utilize all workers.

### asyncio

 - Concurrent task execution (background & foreground).
 - Good for I/O-bound tasks.

### django-rq

 - Concurrent task execution (background & foreground).
 - Can access and modify shared data between tasks using redis.
 - Good for I/O-bound tasks.
 - Has monitoring and retry mechanism.
 - Can utilize all workers.
 - `celery -A my_project worker -l info -P gevent` and `celery -A my_project beat -l info` must be running.

### django-crontab

 - Scheduled tasks (CRON).
 - Good for I/O-bound tasks.
 - Has management.

### django-q

 - Concurrent task execution (background & foreground).
 - Can access and modify shared data between tasks using cache or database.
 - Good for both I/O-bound and CPU-bound tasks.
 - Scheduled tasks (CRON) statically/dynamically using django-q.
 - Has monitoring and management in django-q itself.
 - Can utilize all workers.
 - `python manage.py qcluster` must be running.
