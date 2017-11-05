# coding:utf-8
import hashlib
import os

def myfunc(func):
    for attr in dir(func):
        tempstr = 'print "%s:%s.%s"' % (attr, func.__name__, attr)
        tempcodeobj = compile(tempstr, '', 'single')
        exec tempcodeobj


def printattrs_of_func(func):
    print '*' * 100
    for attrname in dir(func):
        tmpstr = '%s.%s' % (func.__name__, attrname)
        tmpcodeobject = compile(tmpstr, "", "eval")
        print attrname, ":", eval(tmpcodeobject)
    print '*' * 100


def printhelp_of_module(module):
    print '*' * 100
    for item in dir(module):
        tmpstr = '%s.%s' % (module.__name__, item)
        tmpcodeobject = compile(tmpstr, "", "eval")
        print item, ':', eval(tmpcodeobject)
    print '*' * 100


def main():
    exec 'printattrs_of_func(myfunc)'
    exec 'printhelp_of_module(os)'


if __name__ == '__main__':
    main()
