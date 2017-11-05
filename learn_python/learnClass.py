#coding:utf-8
#population是类的变量，相当于C++的类静态变量 name使用self调用，属于对象的变量
class Person:
	'''Represents a person'''
	population=0
	
	def __init__(self,name):
		'''Initializes the person.s data'''
		self.name=name
		print 'Initialize %s'%self.name
		
		#when this person is created, population increase
		Person.population +=1
		
	def __del__(self):
		'''I am dying'''
		print '%s says bye'% self.name
		
		Person.population -= 1
		
		if Person.population==0:
			print 'I am the lastone'
		else:
			print 'There are still %d people left'% Person.population
	
	def sayHi(self):
		print "Hello,how are you ? my name is",self.name
	
	def howMany(self):
		'''Print the current population'''
		
		if Person.population ==1:
			print 'I am the only person here'
		else:
			print 'We have %d person here'% Person.population
	
zhqs=Person("zhqs")
zhqs.sayHi()
zhqs.howMany()

swaroop=Person('Swaroop')
swaroop.sayHi()
swaroop.howMany()

del zhqs

kalam=Person('Kalam')
kalam.sayHi()
kalam.howMany()

del swaroop
