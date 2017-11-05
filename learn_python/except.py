#coding:utf-8

import sys

class ShortInputException(Exception):
	'''A user-defined exception class.'''
	
	def __init__(self, length, atleast):
		Exception.__init__(self)
		self.length=length
		self.atleast=atleast
	

try:
	s=raw_input('Entersomething->')
	if(len(s) < 3):
		raise ShortInputException(len(s), 3)
except EOFError:
		print '\n Why did you do an EOF on me?'
		sys.exit()
except ShortInputException, x:
		print 'ShortInputException: The input was of length %d ,\
			was excepting at least %d'%(x.length, x.atleast)
except:
		print '\nSome error/exception occurred.'
else:
	print 'No exception was raised'
		

import time		
try:
	f=file('poem.txt')
	while True:
		line=f.readline()
		if len(line) == 0:
			break
		time.sleep(1)
		print line
finally:
	f.close()
print 'Done!'

def safe_float(object):
	try:
		retval=float(object)
	except(ValueError, TypeError), diag:
		retval=str(diag)
	return retval
	
if __name__ == '__main__':
	print safe_float("xyz");
	print safe_float({});
	
	try:
		assert 1==0, 'One does not equal zero silly!'
	except AssertionError, args:
		print '%s:%s:%s'%(args.__class__,args.__class__.__name__, args)