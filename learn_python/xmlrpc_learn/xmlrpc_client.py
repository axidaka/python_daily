# coding: utf-8

import  xmlrpclib

proxy = xmlrpclib.ServerProxy("http://localhost:8000/")
print "3 is even:%s" % str(proxy.is_even(3))  #调用远程接口
print "100 is even:%s" % str(proxy.is_even(100))