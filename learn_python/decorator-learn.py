# coding:utf-8

def makebold(fn):
    print "I am a decorator makebold"

    def wrapped():
        return "<b>" + fn() + "</b>"

    return wrapped


def makeitalic(fn):
    def wrapped():
        return "<i>" + fn() + "</i>"

    return wrapped


@makebold
@makeitalic
def hello():
    return "hello world"


# 装饰器高级用法：在装饰器函数传入参数
def a_decorator_passing_args(func_to_decorate):
    def wrapper_accept_args(arg1, arg2):
        print 'I got args! Look:', arg1, arg2
        func_to_decorate(arg1, arg2)

    return wrapper_accept_args


@a_decorator_passing_args
def print_full_name(firstname, lastname):
    print 'My name is', firstname, lastname


# 任意参数
def a_decorator_passing_arbitrary_args(func_to_decorate):
    def a_wrapper_accepting_arbitrary_args(*args, **kwargs):
        print "Do I have args?:"
        print args;
        print kwargs
        func_to_decorate(*args, **kwargs)

    return a_wrapper_accepting_arbitrary_args


@a_decorator_passing_arbitrary_args
def func_with_no_args():
    print "Python is Cool, no args here"


@a_decorator_passing_arbitrary_args
def func_with_args(a, b, c):
    print a, b, c


@a_decorator_passing_arbitrary_args
def func_with_named_args(a, b, c, platypus="Why not ?"):
    print "Do %s, %s and %s like platypus? %s" % (a, b, c, platypus)


class Mary(object):
    def __init__(self):
        self.age = 32

    @a_decorator_passing_arbitrary_args
    def sayYourAge(self, lie=-3):
        print "I am %s, what did you think?" % (self.age + lie)


if __name__ == "__main__":
    print hello()
    print makebold(hello)()
    print makeitalic(hello)()

    makebole_hello = makebold(hello)
    print makebole_hello()

    makeitalic_hello = makeitalic(hello)
    print makeitalic_hello()

    print_full_name("zheng", "qingsong")

    func_with_no_args()
    func_with_args(1, 2, 3)
    func_with_named_args(1, 2, 3, "Inddd")

    Mary().sayYourAge()