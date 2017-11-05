# coding=utf-8

__author__ = "zhqs"
__desc__ = "面向对象编程"


# 6.1温标的转化
class Temperature(object):
    coefficients = {'c': (1.0, 0.0, -273.15), 'f': (1.8, -273.15, 32.0), 'r': (1.8, 0.0, 0.0)}

    def __init__(self, **kwargs):
        """
         默认使用 绝对（开氏)温度0. 可接受 一个命名的参数
         名字可以是 k c f r
        :param kwargs:
        :return:
        """
        try:
            name, value = kwargs.popitem()
        except KeyError:
            # 无参数, 默认是k = 0
            name, value = 'k', 0

        # 参数过多或者参数无法识别, 报错
        if kwargs or name not in self.coefficients:
            kwargs[name] = value
            raise TypeError, "invalid arguments %r" % kwargs
        # 正确则设置
        setattr(self, name, float(value))

    def __getattr__(self, name):
        """
        将 c f r 的获取映射到k的计算中
        :param name: 温标类型 c f r
        :return:
        """
        try:
            eq = self.coefficients[name]
        except KeyError:
            # 未知名字
            raise AttributeError, "Unknow Attribute", name

        return (self.k + eq[1]) * eq[0] + eq[2]

    def __setattr__(self, name, value):
        """
        将对k c f r的设置映射为对K的设置
        :param name:
        :param value:
        :return:
        """
        if name in self.coefficients:
            eq = self.coefficients[name]
            self.k = (value - eq[2]) / eq[0] - eq[1]
        elif name == 'k':
            object.__setattr__(self, name, value)
        else:
            raise AttributeError, name

    def __str__(self):
        # 打印简要信息
        return "%s K" % self.k

    def __repr__(self):
        # 详细信息打印
        return "Temperature(k = %r)" % self.k


# 6.4链式字典查询 (有多个映射, 在这些映射中以链式方式查询, 有就返回, 没有尝试第二个)
class Chainmap(object):
    """
    """

    def __init__(self, *mappings):
        self._mappings = mappings

    def __getitem__(self, item):
        """
        在序列的字典中查询, 没有找到就抛出KeyError
        """
        for mapping in self._mappings:
            try:
                return mapping[item]
            except KeyError:
                pass
        # 执行到这里说明没有找到
        raise KeyError, item

    def get(self, key, default=None):
        """
        若存在key,则返回之.否则返回默认
        """
        try:
            # [] 调用的是__getitem__
            return self[key]
        except KeyError:
            return default

    def __contains__(self, item):
        try:
            self[item]
            return True
        except KeyError:
            return False


# 6.3限制属性设置
def no_new_attributes(wrapped_setattr):
    """
    试图添加新属性时, 报错
    但允许已经存在的属性被随意设置
    :param wrapped_setattr:
    :return:
    """

    def __setattr__(self, name, value):
        if hasattr(self, name):  # 非新属性,允许设置
            wrapped_setattr(self, name, value)
        else:
            raise AttributeError("Cann't add attribute %r to %s" % (name, self))

    return __setattr__


class NoNewAttributes(object):
    """
    NoNewAttributes的子类会拒绝新属性的添加.
    """
    # 设置非新属性时, 调用object.__setattr__
    __setattr__ = no_new_attributes(object.__setattr__)

    class __metaclass__(type):
        # 一个简单的自定义元类, 禁止向类添加属性
        __setattr__ = no_new_attributes(type.__setattr__)


class Person(NoNewAttributes):
    firstname = ''
    lastname = ''

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return 'Person(%r, %r)' % (self.firstname, self.lastname)


# 6.7 有命名子项的数组
# use operator.itemgetter if we're in 2.4, roll our own if we're in 2.3
try:
    from operator import itemgetter
except ImportError:
    def itemgetter(i):
        def getter(self): return self[i]

        return getter


def superTuple(typename, *attribute_names):
    """
    创建并返回拥有名字属性的元组子类,注意返回的是类
    """
    # 给子类合适的 __new__ 和 __repr__特殊方法
    nargs = len(attribute_names)

    class supertup(tuple):
        __slots__ = ()  # 我们不需要每个实例提供一个字典， 节省内存

        def __new__(cls, *args):
            if len(args) != nargs:
                raise TypeError, '%s takes exactly %d arguments (%d given)' % (typename, nargs, len(args))
            return tuple.__new__(cls, args)

        def __repr__(self):
            return '%s(%s)' % (typename, ','.join(map(repr, self)))

    # 给我们的元组子类添加一些键
    for index, attrname in enumerate(attribute_names):
        setattr(supertup, attrname, property(itemgetter(index)))

    supertup.__name__ = typename

    return supertup


# 6.8 避免属性读写的冗余代码, 通过工厂方法来生成 传递属性名字就返回属性读写方法
def xproperty(fget, fset, fdel=None, doc=None):
    if isinstance(fget, str):
        attr_name = fget

        def fget(obj):
            return getattr(obj, attr_name)
    elif isinstance(fset, str):
        attr_name = fset

        def fset(obj, val):
            setattr(obj, attr_name, val)
    else:
        raise TypeError, 'either fget or fset must be a str'
    return property(fget, fset, fdel, doc)

# 6.11 缓存环的实现 (定义固定大小的缓存, 当它被填满时, 新加入的元素会覆盖第一个元素)
# 该数据结构在存储日志和历史信息时非常有用
class RingBuffer(object):
    """这是一个未填满的缓存类"""
    def __init__(self, size_max):
        self.max = size_max
        self.data = []

    class __Full(object):
        """这是一个填满了的缓存类"""
        def append(self, x):
            """新加入的元素会覆盖掉最旧的元素"""
            self.data[self.cur] = x
            self.cur = (self.cur + 1) % self.max

        def tolist(self):
            return  self.data[self.cur:] + self.data[:self.cur]

    def append(self, x):
        """在缓存末尾添加一个元素"""
        self.data.append(x);
        if len(self.data) == self.max:
            self.cur = 0
            # 永久性将self的类从非满改成满
            self.__class__ = self.__Full

    def tolist(self):
        return self.data

# 6.12 检查一个实例的状态变化
import copy
class ChangeCheckerMixin(object):
    containerItems = {dict: dict.iteritems, list: enumerate}
    immutable = False

    def snapshot(self):
        if self.immutable:
            return
        self._snapshot = self._copy_container(self.__dict__)

    def makeImmutable(self):
        self.immutable = True
        try:
            del self._snapshot
        except AttributeError:
            pass

    def _copy_container(self, container):
        """半浅拷贝， 只对容器类型递归"""
        new_container = copy.copy(container)
        for k, v in self.containerItems[type(new_container)](new_container):
            if type(v) in self.containerItems:
                new_container[k] = self._copy_container(v)
            elif hasattr(v, 'snapshot'):
                v.snapshot()
        return new_container

    def isChanged(self):
        """从上次快照之后，如果有变化就返回true"""
        if self.immutable:
            return False
        # 从self.__dict__ 中删除快照， 并置于末尾
        snap = self.__dict__.pop('_snapshot', None)
        if snap is None:
            return True
        try:
            return self._checkContainer(self.__dict__, snap)
        finally:
            self._snapshot = snap

    def _checkContainer(self, container, snapshot):
        """如果容器和快照不同， 返回True"""
        if len(container) != len(snapshot):
            return True
        for k, v in self.containerItems[type(container)](container):
            try:
                ov = snapshot[k]
            except LookupError:
                return True
            if self._checkItem(v, ov):
                return True
        return False

    def _checkItem(self, newitem, olditem):
        """比较新旧元素， 如果它们是容器类型，递归调用"""
        if type(newitem) != type(olditem):
            return True
        if type(newitem) in self.containerItems:
            return self._checkContainer(newitem, olditem)
        if newitem is olditem:
            method_isChanged = getattr(newitem, 'isChanged', None)
            if method_isChanged is None:
                return False
            return method_isChanged()
        return newitem != olditem

def main():
    t1 = Temperature(f=333)
    print t1.k, t1.c, t1.f, t1.r

    t2 = Temperature(c=333)
    print t2

    t2.k = 333
    print t2
    print t2.c

    import const, sys
    # const.magic = 23
    # const.magic = 444
    # del const.magic

    print u'测试链式字典查询----------------------'
    import __builtin__
    pylookup = Chainmap(locals(), globals(), vars(__builtin__))
    print pylookup['__name__']
    print pylookup.get("__name__", "hahah")
    print '__name__' in pylookup

    print u'测试限制属性的设置'
    me = Person('真', '清松')
    print me
    me.firstname = '郑'
    print me
    try:
        me.age = 30
    except AttributeError, err:
        print 'raise %r as excepted' % err

    print u'测试有命名子项的元组'
    # xian创建带属性名称得到类
    Point = superTuple('Point', 'x', 'y')
    print Point
    # 创建对象， 为属性赋值
    p = Point(1, 2)
    print p.x, p.y

    try:
        pErr = Point(1, 2, 3)
    except TypeError, e:
        print e

    print u'测试6.8避免属性读写的冗余代码'

    class Lower(object):
        def __int__(self, s=''):
            self._s = s

        def _setS(self, s):
            self._s = s.lower()

        s = xproperty('_s', _setS)

    lower_test = Lower()
    lower_test.s = 'Zhqs'
    print lower_test.s

    print u'测试 6.10保留对绑定方法的引用且支持垃圾回收'

    class C(object):
        def f(self):
            print 'hello'
        def __del__(self):
            print 'C dying'

    import weakmethod
    c = C()
    print type(c.f)
    cf = weakmethod.ref(c.f)
    cf()()
    del c
    print cf()

    print u'测试 6.11缓存环的实现'
    x = RingBuffer(5)
    for i in range(1, 5):
        x.append(i)
    print x.__class__, x.tolist()
    x.append(5)
    print x.__class__, x.tolist()

    x.append(6)
    print x.__class__, x.data, x.tolist()
    x.append(7);x.append(8);x.append(9);x.append(10)
    print x.data, x.tolist()

    print u'测试 6.12 检查一个实例的状态变化'
    class eg(ChangeCheckerMixin):
        def __init__(self, *a, **k):
            self.L = list(*a, **k)
        def __str__(self):
            return 'eg(%s)' % str(self.L)
        def __getattr__(self, a):
            return getattr(self.L, a)

    x = eg('ciao')
    print 'x =', x, 'is changed =', x.isChanged()
    # emits: x = eg(['c', 'i', 'a', 'o']) is changed = True
    # now, assume x gets saved, then...:
    x.snapshot()
    print 'x =', x, 'is changed =', x.isChanged()
    # emits: x = eg(['c', 'i', 'a', 'o']) is changed = False
    # now we change x...:
    x.append('x')
    print 'x =', x, 'is changed =', x.isChanged()
    # emits: x = eg(['c', 'i', 'a', 'o', 'x']) is changed = True

if __name__ == "__main__":
    main()
