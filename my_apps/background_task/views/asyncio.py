from django.views import View
from django.http import JsonResponse
import asyncio
from asgiref.sync import async_to_sync


async def my_async_function1(*args, **kwargs):
    print('function 1', args, kwargs)
    for i in range(1, 6):
        print(i)
        await asyncio.sleep(1)
    return 1


async def my_async_function2(*args, **kwargs):
    print('function 2', args, kwargs)
    for i in range(1, 6):
        print(i)
        await asyncio.sleep(1)
    return 2


class AsyncioView(View):
    """
    This doesn't run the task in the background.
    But, We can run multiple tasks simultaneously.
    """
    @async_to_sync
    async def post(self, request):
        loop = asyncio.get_event_loop()
        task1 = loop.create_task(my_async_function1(1, 2, x=3))
        task2 = loop.create_task(my_async_function2(1, 2, x=3))
        await asyncio.gather(task1, task2)
        result1 = await task1
        result2 = await task2
        print('result', result1, result2)

        return JsonResponse({'success': True}, status=200)
