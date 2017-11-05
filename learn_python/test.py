#coding:utf-8

import platform;

def displayNumType(num):
	print num, 'is',
	if isinstance(num, (int, long, float, complex)):
		print 'a number of type:', type(num).__name__
	else:
		print 'not a number at all!'
	
#function defintion
def sayHello():
	print "Hello World! This is my first Python Function"

def printMax(x, y):
	'''Print the maximum of two numbers
	
	The two values must be integers'''
	x=int(x)
	y=int(y)
	
	if x >y :
		print x,"is max"
	else:
		print y,"is max"

def foo():
	m = 3
	
	def bar():
		n = 4
		print m + n
		
	print m, bar()

def hellocounter(name):
	count= [0]
	def counter():
		count[0] += 1
		print 'Hello:', name, str(count[0]), 'access!'

	return counter

j, k = 1, 2

def proc1():
	j, k = 3, 4
	print 'j==%d and k == %d'%(j, k)
	k = 5

def proc2():
	j = 6
	proc1()
	print 'j==%d and k == %d'%(j, k)

if __name__ == '__main__':

	proc2()

	foo()

	hello = hellocounter('zqs')
	hello()
	hello()
	hello()

	displayNumType(233);
	displayNumType(9999999999999999L)
	displayNumType(98.55)
	displayNumType(-5.2+1.9j)
	displayNumType('xxxx')
	
	print "Just for demo how to do python development under windows:"
	print "uname=", platform.uname()
	lenght=5
	breadth=2
	area=lenght*breadth
	print 'Area is', area, " lenght is ", lenght
	
	number=23
	running=True

	while running:
		guess=int(raw_input("Enter an integer:"))

		if guess== number:
			print "Congratulations,you guess it."
			print "(but you dot not win any prizes!)"
			running=False
		elif guess < number:
			print "No, it is a litter higher than that"
		else:
			print "No, it is a litter lower than that"
	else:
		print "The While Loop is Over."
		
	for index in range(5):
		print index
	else:
		print "The for loop is over"
		
	for index2 in range(1,5):
		print index2
	else:
		print "The for loop is over"
		
	for index3 in range(2,8,2):
		print index3
	else:
		print "The for loop is over"
		
	while True:
		s=raw_input("Enter something:")
		if s== "quit":
			break
		if len(s) < 3:
			continue
		print "Length of the string is", len(s)
		
	sayHello();

	printMax(3, 5)

	print "DocStrings test:",printMax.__doc__

	help('printMax')
	print "Done"