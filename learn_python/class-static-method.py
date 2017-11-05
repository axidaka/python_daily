# coding:utf-8

# 类方法（class method)可以被类和类实例调用，类方法的调用参数是类，派生类调用时传入的是该派生类静态方法（static method）
# 可以被类和类实例调用，没有调用参数二者均不可以访问实例变量，如self.name


class TestClassMethod(object):

    METHOD = 'method hoho'

    def __init__(self):
        self.name = 'zqs'

    def test1(self):
        print 'instance method'
        print 'name:', self.name, self
        print 'class attribute:', TestClassMethod.METHOD

    @classmethod
    def test2(cls):
        print cls
        print 'test2'
        print TestClassMethod.METHOD
        print '-----fen ge---------'

    @staticmethod
    def test3():
        print TestClassMethod.METHOD
        print 'test3'


class RoundFloadManual(object):

    def __init__(self, val):
        assert isinstance(val, float)
        self.value = round(val, 2)

    def __str__(self):
        return '%.2f' % self.value

    __repr__ = __str__


def testMyFloat():
    rfm = RoundFloadManual(5.66344)
    print rfm
    # rfm


class Time60(object):

    """Time60 - track hours and miniutes"""

    def __init__(self, hr, min):
        self.hr = hr
        self.min = min

    def __str__(self):
        'Time60 - string representation'
        return '%d:%d' % (self.hr, self.min)

    __repr__ = __str__

    def __add__(self, other):
        'Time60- overloading the addition operator'
        return self.__class__(self.hr + other.hr, self.min + self.min)

    def __iadd__(self, other):
        'Time60-overloading in-place addition'
        self.hr += other.hr
        self.min += other.min
        return self


def TestTime60():
    mon = Time60(10, 20)
    tue = Time60(11, 15)
    print mon, tue
    print 'mon:', id(mon)
    print mon + tue
    mon += tue
    print 'mon:', id(mon)
    print mon, tue


class AnyIter(object):

    """docstring for AnyIter"""

    def __init__(self, data, safe=False):

        self.iter = iter(data)
        self.safe = safe

    def __iter__(self):
        return self

    def next(self, howmany=1):
        retval = []
        for eachItem in range(howmany):
            try:
                retval.append(self.iter.next())
            except StopIteration:
                if self.safe:
                    break
                else:
                    raise
        return retval


def TestAnyIter():

    b = AnyIter(range(10), True)
    bi = iter(b)
    for bj in range(6):
        print bj, ':', bi.next(bj)

    a = AnyIter(range(10))
    i = iter(a)
    for j in range(1, 6):
        print j, ':', i.next(j)

    # print i.next(10)


def main():
    test = TestClassMethod()
    test.test1()
    print '-------------------'
    test.test2()
    print '-------------------'
    test.test3()

    print '-------------------'
    TestClassMethod.test2()
    TestClassMethod.test3()

if __name__ == '__main__':
    # main()
    # testMyFloat()
    # TestTime60()
    TestAnyIter()
