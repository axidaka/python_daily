# coding:utf-8

import thread
import threading
from time import sleep, ctime

loops = [4, 2]


def thread_loop(nloop, nsec, lock):
    print 'start loop', nloop, ctime()
    sleep(nsec)
    print 'loop', nloop, 'done at', ctime()
    lock.release()


def thread_maintest():
    print 'starting at:', ctime()
    locks = []
    nloops = range(len(loops))

    for i in nloops:
        lock = thread.allocate_lock()
        lock.acquire()
        locks.append(lock)

    for i in nloops:
        thread.start_new_thread(thread_loop, (i, loops[i], locks[i]))

    for i in nloops:
        while locks[i].locked():  # 当前锁对象还被其他现成占用返回True
            pass

    print 'all Done at:', ctime()


def threading_loop(nloop, nsec):
    print 'start loop', nloop, 'at:', ctime()
    sleep(nsec)
    print 'loop', nloop, 'done at:', ctime()


def threading_maintest1():
    print 'starting at:', ctime()
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        # 创建一个Thread的实例，传递函数threading_loop做为run后续调用
        t = threading.Thread(target=threading_loop, args=(i, loops[i]))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:  # wait for all thread exist
        threads[i].join()

    print 'all Done at', ctime()


class ThreadFunc(object):

    """可执行对象，用于传递给threading.Thread构造函数target参数"""

    def __init__(self, func, args, name=''):
        super(ThreadFunc, self).__init__()
        self.func = func
        self.args = args
        self.name = name

    def __call__(self):
        apply(self.func, self.args)


def threading_maintest2():
    print 'starting at:', ctime()
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        # 创建一个Thread的实例，传递一个可调用的类对象
        t = threading.Thread(
            target=ThreadFunc(threading_loop, (i, loops[i]), threading_loop.__name__))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print 'all Done at:', ctime()


class MyThread(threading.Thread):

    """Thread派生类"""

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name

    def run(self):
        apply(self.func, self.args)


def threading_maintest3():
    print 'starting at:', ctime()
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        # 创建一个Thread的实例，传递一个可调用的类对象
        t = MyThread(threading_loop, (i, loops[i]), thread_loop.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print 'all Done at:', ctime()

if __name__ == '__main__':
    # thread_maintest()
    # threading_maintest1()
    # threading_maintest2()
    threading_maintest3()
