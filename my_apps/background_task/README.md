# Background Tasks

---
## Inbuilt

### threading

 - Concurrent task execution.
 - It shares common memory space.
 - Good for I/O-bound tasks but not for CPU-bound tasks due to GIL.
 - Can access and modify shared data between tasks.

### concurrent.futures.ThreadPoolExecutor

 - Concurrent execution using a pool of threads.
 - Shares memory space (GIL-bound).
 - Good for I/O-bound tasks.
 - High-level abstraction over threading.

### multiprocessing

 - Parallel task execution.
 - Each process has its own memory space.
 - Good for CPU-bound tasks as it can utilize multiple CPUs.
 - Can access and modify shared data between tasks using shared memory, queues or pipes.

### concurrent.futures.ProcessPoolExecutor

 - Parallel task execution using a pool of processes.
 - High-level abstraction over multiprocessing.
 - Good for CPU-bound tasks.
 - Easier to use than raw multiprocessing.

### asyncio

 - Concurrent, single-threaded asynchronous task execution.
 - Uses coroutines, event loop, and non-blocking I/O.
 - Great for I/O-bound tasks like network requests, DB calls.
 - Not suitable for CPU-heavy operations.

---
## 3rd Party

### joblib

 - Parallel execution using multiple processes.
 - Simplifies parallelization of loops and heavy computations.
 - Common in scientific computing (e.g., scikit-learn model training).
 - Can also use threading for I/O-bound tasks with backend='threading'.

### dask

 - Parallel and distributed task execution.
 - Supports dynamic task graphs, delayed execution, and large datasets.
 - Scales from threads to processes to distributed clusters.
 - Used for big data, machine learning, and dataframes.

### celery

 - Distributed task queue for concurrent or parallel execution (only background).
 - Can access and modify shared data between tasks using `redis`, rabbitmq, cache or database.
 - Good for both I/O-bound and CPU-bound tasks.
 - Can have Scheduled tasks (CRON) statically using celery itself, dynamically using `django-celery-beat`.
 - Has monitoring and management using `flower`, retry mechanism and prioritization.
 - Can utilize all workers.
 - `celery -A my_project worker -l info -P gevent` and `celery -A my_project beat -l info` must be running.

### apscheduler

 - Scheduled tasks (CRON, Interval, ...) (only background).
 - It supports both sync and async job execution.
 - Good for I/O-bound tasks but not for CPU-bound tasks due to single-threaded nature.
 - Has management - Can add, modify, and remove scheduled tasks dynamically.
 - Runs in background within apps (like Flask/Django).

### django-rq

 - Concurrent or parallel task execution based on worker setup (only background).
 - Can access and modify shared data between tasks using redis.
 - Good for I/O-bound tasks.
 - Has monitoring and retry mechanism.
 - Can utilize all workers.
 - `python manage.py rqworker` must be running.

### django-crontab

 - Scheduled tasks for Django (CRON) (only background).
 - Good for I/O-bound tasks.
 - Management via Django settings and manage.py crontab commands.

### django-q

 - Concurrent or parallel task execution (thread or process-based workers) (only background).
 - Can access and modify shared data between tasks using database or message broker.
 - Good for both I/O-bound and CPU-bound tasks.
 - Scheduled tasks (CRON) statically/dynamically using django-q.
 - Has monitoring and management in django-q itself.
 - Can utilize all workers.
 - `python manage.py qcluster` must be running.


## Differences

| Package             | Type      | Concurrent      | Parallel        | Scheduling      | Notes                                                 |
|---------------------|-----------|-----------------|-----------------|-----------------|-------------------------------------------------------|
| threading           | Inbuilt   | ✓               | ✖               | ✖               | I/O-bound; shares memory; affected by GIL             |
| ThreadPoolExecutor  | Inbuilt   | ✓               | ✖               | ✖               | I/O-bound; concurrent threads; GIL-limited            |
| multiprocessing     | Inbuilt   | ✖               | ✓               | ✖               | CPU-bound; separate memory; true parallel             |
| ProcessPoolExecutor | Inbuilt   | ✖               | ✓               | ✖               | CPU-bound; high-level parallel processing             |
| asyncio             | Inbuilt   | ✓               | ✖               | ✖               | I/O-bound; single-threaded async; non-blocking        |
| joblib              | 3rd-Party | ✓ (with config) | ✓ (default)     | ✖               | CPU or I/O-bound; simple parallel loops               |
| dask                | 3rd-Party | ✓               | ✓               | ✓               | Scalable; big data; task graphs; distributed          |
| celery              | 3rd-Party | ✓               | ✓               | ✓               | I/O and CPU-bound; distributed; broker-based          |
| apscheduler         | 3rd-Party | ✓ (default)     | ✓ (with config) | ✓               | I/O-bound; uses threads by default, can use processes |
| django-rq           | 3rd-Party | ✓               | ✓ (with config) | ✓ (with config) | I/O-bound; Redis-backed queue                         |
| django-crontab      | 3rd-Party | ✖               | ✖               | ✓               | I/O-bound; system-level cron integration              |
| django-q            | 3rd-Party | ✓               | ✓               | ✓               | I/O and CPU-bound; thread or process workers          |
