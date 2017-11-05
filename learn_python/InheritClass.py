#coding:utf-8

#类的继承

class SchoolMember:
	'''Represents any school member'''
	def __init__(self,name,age):
		self.name=name
		self.age=age
		print '(Initialized SchoolMember:%s)'% self.name
	
	def tell(self):
		'''Tell my details'''
		print 'Name:%s Age:%s'%(self.name,self.age)
	

class Teacher(SchoolMember):
	'''Represents teacher'''
	def __init__(self,name,age,salary):
		SchoolMember.__init__(self,name,age)
		self.salary=salary
		print '(Initialized Teacher:%s)'% self.name
	
	def tell(self):
		SchoolMember.tell(self)
		print 'Salary:%d'% self.salary
	
class Student(SchoolMember):
	'''Represents student'''
	def __init__(self,name,age,marks):
		SchoolMember.__init__(self,name,age)
		self.marks=marks
		print'(Initialized Studeng:%s)'% self.name
	
	def tell(self):
		SchoolMember.tell(self)
		print 'Marks:%d'% self.marks

	
t=Teacher('Mrs.Zh',40,200000)
s=Student('Swaroop',22,100)

print

members=[t,s]
for member in members:
	member.tell()