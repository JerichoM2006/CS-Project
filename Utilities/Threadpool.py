import concurrent
import concurrent.futures

from Utilities.Singleton import Singleton

class Threadpool(Singleton):
    def initialise(self, max_workers : int) -> None:
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.workers = dict()

    def submit(self, func, *args, **kwargs):
        name = func.__name__
        index = 1
        while True:
            if name in self.workers:
                index += 1
                name = func.__name__ + str(index)
            else:
                break
        
        self.workers[name] = self.executor.submit(func, *args, **kwargs)
        return self.workers[name]
    
    def getResult(self, name):
        if name not in self.workers:
            raise Exception("Worker not found")
        
        return self.workers[name].result()

    def __del__(self):
        self.executor.shutdown()
