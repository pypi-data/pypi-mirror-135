from concurrent.futures import ThreadPoolExecutor
from threading import BoundedSemaphore


class AsyncExecuter:
    """
    BoundedExecutor behaves as a ThreadPoolExecutor which will block on
    calls to submit() once the limit given as "bound" work items are queued for
    execution.

    :param bound: Integer - the maximum number of items in the work queue
    :param max_workers: Integer - the size of the thread pool
    """

    def __init__(self, bound=100, max_workers=8):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.semaphore = BoundedSemaphore(bound + max_workers)

    def submit(self, fn, *args, **kwargs):
        self.semaphore.acquire()
        try:
            future = self.executor.submit(fn, *args, **kwargs)
        except:
            self.semaphore.release()
            raise
        else:
            future.add_done_callback(lambda x: self.semaphore.release())
            return future

    def shutdown(self, wait=False):
        self.executor.shutdown(wait)
