''' run in thread or not '''
from threading import Thread, Lock

class ThreadObj:
    ''' just to easy turn on and turn of thread '''
    def __init__(self, turn_on : bool = False):
        if turn_on:
            print('Subactions will run as thread')
            self.thread_start = lambda action : Thread(target = action).start()
            lock = Lock()
            self.acquire = lock.acquire
            self.release = lock.release
        else:
            print('Subactions will run without thread')
            self.thread_start = lambda action : action()
            self.acquire = lambda : None
            self.release = lambda : None
