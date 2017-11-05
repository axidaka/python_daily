# coding=utf-8

__author__ = "zhqs"
__desc__ = "进程 线程 同步"


# 9.1同步对象中的所有方法
def wrap_callable(any_callable, before, after):
    """使用before/after调用将任何可调用封装起来"""

    def _wrapped(*a, **kw):
        before()
        try:
            return any_callable(*a, **kw)
        finally:
            after()

    return _wrapped


import inspect


class GenericWrapper(object):
    """将对象所有的方法用before/after调用封装起来"""

    def __init__(self, obj, before, after, ignore=()):

        classname = 'GenericWrapper'  # 用于双下划线 变量扎压
        self.__dict__['_%s__methods' % classname] = {}
        self.__dict__['_%s__obj' % classname] = obj
        for name, method in inspect.getmembers(obj, inspect.ismethod):
            if name not in ignore and method not in ignore:
                self.__methods[name] = wrap_callable(method, before, after)

    def __getattr__(self, item):
        try:
            return self.__methods[item]
        except KeyError:
            return getattr(self.__obj, item)

    def __setattr__(self, key, value):
        setattr(self.__obj, key, value)


class SynchronizedObject(GenericWrapper):
    """封装一个对象及其所有方法, 支持同步"""

    def __init__(self, obj, ignore, lock=None):
        if lock is None:
            import threading
            lock = threading.RLock()
        GenericWrapper.__init__(self, obj, lock.acquire, lock.release, ignore)


# 9.2 终止线程
import threading


class TestThead(threading.Thread):
    def __init__(self, name="TestThread"):
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        threading.Thread.__init__(self, name=name)

    def run(self):
        """主循环"""
        print "%s starts " % (self.getName(),)
        count = 0
        while not self._stopevent.isSet():
            count += 1
            print "loop %d" % (count,)
            self._stopevent.wait(self._sleepperiod)
        print "%s ends" % (self.getName(),)

    def join(self, timeout=None):
        self._stopevent.set()
        threading.Thread.join(self, timeout)


def main():
    print u'测试同步对象中所有方法'
    import threading, time
    class Dummy(object):
        def foo(self):
            print 'hello from foo'
            time.sleep(1)

        def bar(self):
            print 'hello from bar'

        def baaz(self):
            print 'hello from baaz'

    tw = SynchronizedObject(Dummy(), ignore={'baaz'})
    threading.Thread(target=tw.foo).start()
    time.sleep(0.1)
    threading.Thread(target=tw.bar).start()
    time.sleep(0.1)
    threading.Thread(target=tw.baaz).start()

    print u'测试终止线程'
    testthread = TestThead()
    testthread.start()
    import time
    time.sleep(5.0)
    testthread.join()


if __name__ == "__main__":
    main()
