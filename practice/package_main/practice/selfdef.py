# coding:utf-8

import StringIO


def item_of_module(module):
    for item in dir(module):
        print item


def item_of_dict(dictobj):
    for (k, v) in dictobj.items():
        print '(%s):(%s)' % (k, v)


def traverse_sequence(seq):
    for item in seq:
        print item


def addsyspath(new_path):
    """给Python的sys.path增加目录"""

    import sys
    import os

    if not os.path.exists(new_path):
        return -1

    # 将路径标准化，windows是大小写不敏感的，所以若确定在window下，将其转化成小写
    new_path = os.path.abspath(new_path)

    if sys.platform == 'win32':
        new_path = new_path.lower()

    # 检查所有的路径
    for x in sys.path:
        x = os.path.abspath(x)
        if sys.platform == 'win32':
            x = x.lower()
        if new_path in (x, x + os.sep):
            return 0
    sys.path.append(new_path)
    return 1

def GetCallStack():
    import sys, os
    retStr = ""
    f = sys._getframe()
    f = f.f_back  # first frame is detailtrace, ignore it
    while hasattr(f, "f_code"):
        co = f.f_code

        fun_key = "%s(%s:%s)" % (os.path.basename(co.co_filename),
                                  co.co_name,
                                  f.f_lineno)

        all_key_value = ""
        for itemkey in f.f_locals:
            key_value = "\t\t %s:%s\n"%(itemkey, f.f_locals[itemkey])
            all_key_value = all_key_value + key_value

        subinfo = "\n(%s:\n\t {locals:\n %s\t}\n)"%(fun_key, all_key_value)

        retStr = subinfo+ retStr

        f = f.f_back
    return retStr


def main():
    new_path = r'G:\代码\taocode\python_project\trunk\learn python'
    import os
    for root, subdirs, files in os.walk(new_path.decode('utf-8').encode('gbk')):
        for itemsubdir in subdirs:
            print 'new_path:', os.path.join(root, itemsubdir)
            addsyspath(os.path.join(root, itemsubdir))


if __name__ != '__main__':
    main()
