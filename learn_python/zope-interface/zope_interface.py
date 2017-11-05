#coding=utf-8

import zope.interface
from zope.interface import Interface, Attribute, implements

#通过Interface继承 定义接口
class IFoo(Interface):
    """Foo blah blah"""

    x = Attribute("""X blah blah""")

    # 方法没有self参数
    def bar(q, r = None):
        """bar blah blah"""


class FOO:
    implements(IFoo)

    def __init__(self, x = None):
        self.x = x

    def bar(self, q, r=None):
        return  q, r, self.x

    def __repr__(self):
        return "FOO(%s)"%self.x

class IFooFactory(Interface):
    """Create foos"""

    def __call__(x = None):
        """
        Create a foo
        The argument provides the initial value for x
        :return:
        """



if __name__ == "__main__":

    for item in dir(IFoo):
        print item
    print '----------------------------'
    print type(IFoo)
    print IFoo.__name__
    print IFoo.__doc__
    print IFoo.__module__

    x = IFoo['x']
    print type(x), 'name:', x.__name__, 'doc:' ,x.__doc__

    print IFoo.get('x').__name__

    print 'x' in IFoo
    print 'y' in IFoo

    try:
        IFoo.x
    except AttributeError:
        print "无法通过接口属性来访问属性"


    # an interface whether it is implemented by a class:
    print IFoo.implementedBy(FOO)

    # whether an interface is provided by an object:
    foo = FOO()
    print IFoo.providedBy(foo)

    print  list(zope.interface.implementedBy(FOO))
    print  list(zope.interface.providedBy(foo))

    # 直接通过使用
    zope.interface.directlyProvides(FOO, IFooFactory)
    print list(zope.interface.providedBy(FOO))
    IFooFactory.providedBy(FOO)
