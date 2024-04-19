# Background Tasks

---
## Inbuilt

### Threading

 - Concurrent task execution (background & foreground).
 - Can access and modify shared data between tasks.
 - Good for I/O-bound tasks but not for CPU-bound tasks due to GIL.
 - It shares common memory space.

### Multiprocessing

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

### Celery

 - Concurrent task execution (background & foreground).
 - Can access and modify shared data between tasks using redis, rabbitmq or database.
 - Good for both I/O-bound and CPU-bound tasks.
 - Can have Scheduled tasks (CRON) with management using django-celery-beat.
 - Has monitoring, management, retry mechanism and prioritization.
 - Can utilize workers.

### Asyncio

 - Concurrent task execution (background & foreground).
 - Good for I/O-bound tasks.

### django-rq

 - Concurrent task execution (background & foreground).
 - Can access and modify shared data between tasks using redis.
 - Good for I/O-bound tasks.
 - Has monitoring and retry mechanism.
 - Can utilize workers.

### django-crontab

 - Scheduled tasks (CRON).
 - Good for I/O-bound tasks.
 - Has management.

### Django-Q

 - Concurrent task execution (background & foreground).
 - Can access and modify shared data between tasks using database.
 - Good for both I/O-bound and CPU-bound tasks.
 - Scheduled tasks (CRON).
 - Has monitoring, management and prioritization.
 - Can utilize workers.
