from django.views import View
from django.http import JsonResponse
import time
import multiprocessing


def my_function1(*args, **kwargs):
    print('function 1', args, kwargs)
    for i in range(1, 6):
        print(i)
        time.sleep(1)
    return 1


def my_function2(*args, **kwargs):
    print('function 2', args, kwargs)
    for i in range(1, 6):
        print(i)
        time.sleep(1)
    return 2


class MultiProcessingView(View):
    """
    Multiprocess - Inbuilt

    Need to comment django_q imports.
    """
    def post(self, request):
        background_def()
        same_def_parallel()
        different_def_parallel()
        InterProcessQueue().start()
        SharedMemory().start()

        return JsonResponse({'success': True}, status=200)


# processors
def background_def():
    """
    Running multiple tasks simultaneously in the background.
    """
    process1 = multiprocessing.Process(target=my_function1, args=(1, 2), kwargs={'x': 3})
    process2 = multiprocessing.Process(target=my_function2, args=(1, 2), kwargs={'x': 3})

    process1.start()
    process2.start()

    # you can terminate the process
    # time.sleep(1)
    # process.terminate()


def same_def_parallel():
    """
    Runs same function simultaneously in the foreground.
    """
    pool = multiprocessing.Pool()
    results = pool.map(my_function1, [(1, 2, {'x': 3}), (4, 5, {'x': 6})])  # triggers 2 times

    pool.close()
    pool.join()  # what ever logic written after join will run once the multiprocess is done.
    print('same function in parallel: ', results)
    return results


def different_def_parallel():
    """
    Runs different functions simultaneously in the foreground.
    """
    pool = multiprocessing.Pool()
    results1 = pool.apply_async(my_function1, args=(1, 2), kwds={'x': 3})
    results2 = pool.apply_async(my_function2, args=(1, 2), kwds={'x': 3})

    results1 = results1.get()
    results2 = results2.get()

    pool.close()
    pool.join()
    print('different function in parallel: ', results1, results2)
    return results1, results2


class InterProcessQueue:
    """
    Different processes will communicate with each other and share data using queue (inter-process communication).
    It is a queue, so it is sync and fifo.
    """

    def start(self):
        input_queue = multiprocessing.Queue()
        output_queue = multiprocessing.Queue()
        process1 = multiprocessing.Process(target=self.q_function1, args=(input_queue,))
        process2 = multiprocessing.Process(target=self.q_function2, args=(input_queue, output_queue))

        process1.start()
        process2.start()

        process1.join(timeout=None)  # you can set the timeout for the process
        input_queue.put(None)  # make sure to break the loop and then .join()
        process2.join()

        results = []
        while not output_queue.empty():
            result = output_queue.get()
            results.append(result)

        print("queue results: ", results)
        return results

    @staticmethod
    def q_function1(q):
        for i in range(3):
            print('sender: ', i)
            q.put(i)
            time.sleep(1)

    @staticmethod
    def q_function2(q_in, q_out):
        while True:
            i = q_in.get()
            if i is None:
                break
            print('receiver: ', i)
            result = my_function1(i)
            q_out.put(result)


class SharedMemory:
    """
    Multiple processes can access and modify the shared data.
    """

    def start(self):
        shared_value = multiprocessing.Value('i', 0)  # 'i' for int, 'c' for char, ...
        shared_list = multiprocessing.Manager().list()
        processes1 = multiprocessing.Process(target=self.update_shared_value, args=(shared_value, shared_list))
        processes2 = multiprocessing.Process(target=self.update_shared_value, args=(shared_value, shared_list))

        processes1.start()
        processes2.start()

        processes1.join()
        processes2.join()
        print(f"Shared value: {shared_value.value}, Shared list: {shared_list}")
        return shared_value.value, shared_list

    @staticmethod
    def update_shared_value(shared_value, shared_list):
        shared_value.value += 1
        shared_list.append(shared_value.value)
