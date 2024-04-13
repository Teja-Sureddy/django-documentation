"""
threading:
Background tasks (concurrent), not for CPU-bound tasks due to GIL.

django-q:
Background tasks (concurrent or single, depends on worker), Scheduling tasks, Task prioritization, Monitoring.

asyncio:
Multiple tasks (concurrent), async I/O - reading files, db & network calls.

multiprocess:
Background tasks (concurrent), Multiple tasks (concurrent), shared memory, suitable for CPU-bound tasks.
"""