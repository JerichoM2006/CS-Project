import concurrent
import concurrent.futures

from Utilities.Singleton import Singleton

class Threadpool(Singleton):
    # Initialises the thread pool
    # max_workers: Maximum number of threads that can be used
    def initialise(self, max_workers : int) -> None:
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.workers = dict()
    
    # Submits a function to the thread pool
    def submit(self, func, *args, **kwargs):
        name = func.__name__
        index = 1
        # Finds a unique name for the worker
        while True:
            if name in self.workers:
                index += 1
                name = func.__name__ + str(index)
            else:
                break
        
        # Submits the function and stores the future
        self.workers[name] = self.executor.submit(func, *args, **kwargs)
        return self.workers[name]
    
    # Gets the result of a worker
    def getResult(self, name):
        # Checks if the worker exists
        if name not in self.workers:
            raise Exception("Worker not found")
        
        # Returns the result of the worker
        return self.workers[name].result()
    
    # Shuts down the thread pool
    def __del__(self):
        self.executor.shutdown()
