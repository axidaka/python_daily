# -*- coding: UTF-8 -*-
# Filename: weakmethod.py

# 6.10 保留被绑定方法的引用且支持垃圾回收
# 弱引用（weak reference）在一个对象处于生存时期指向该对象。但如果没有其他正常的引用指针指向
# 该对象时， 这个对象不会被保留
import weakref, new
class ref(object):
    """
    能够封装任何可调用体， 特别是被绑定方法， 而且被绑定方法仍然能够被回收处理，
    于此同时， 提供一个普通的弱引用的接口
    """
    def __init__(self, fn):
        try:
            # try getting object, function, and class
            o, f, c = fn.im_self, fn.im_func, fn.im_class
        except AttributeError:                # It's not a bound method
            self._obj = None
            self._func = fn
            self._clas = None
        else:                                 # It is a bound method
            if o is None: self._obj = None    # ...actually UN-bound
            else: self._obj = weakref.ref(o)  # ...really bound
            self._func = f
            self._clas = c

    def __call__(self):
        if self._obj is None: return self._func
        elif self._obj() is None: return None
        return new.instancemethod(self._func, self._obj(), self._clas)