#coding:utf-8

poem=''' \
Programming is fun
When the work is done
if you want make your work also fun:
	use Python!
'''

f=file('poem.txt', 'w')
f.write(poem)
f.close()

f=file('poem.txt', 'r')
while True:
	line=f.readline()
	if len(line)==0:
		break
	print line,
f.close()

#储存与取储存

import cPickle as p

shoplistfile='shoplist.data'

shoplist=['apple','mango','carrot']

#write to the file
f=file(shoplistfile, 'w')
p.dump(shoplist, f) #dump the object to a file
f.close()

del shoplist #remove the shoplist

#read back from the storage
f=file(shoplistfile)
storedlist=p.load(f)
f.close()
print 'the shoplist store in the file:', storedlist


class SerializaTest:

	def __init__(self):
		self.name='zqs'
		self.age=123
		print 'SerializaTest Init %s-%d'%(self.name, self.age)
	
	def __del__(self):
		print 'SerializaTest del'
	
	def setAge(self, _age):
		self.age=_age
	
	def printAge(self):
		print '%s my age: %d'%(self.name, self.age)
		
sTest=SerializaTest()
sTest.printAge()
sTest.setAge(23)
sTest.printAge()

f=file('SerializaTestfile.data', 'w')
p.dump(sTest, f)
f.close()

del sTest

f=file('SerializaTestfile.data', 'r')
sLoad=p.load(f)
sLoad.printAge()

#提示用户输入文字，创建文件
import os
ls=os.linesep

#get filename
while True:
	filename=raw_input('Enter a new file name')
	if os.path.exists(filename):
		print 'Error: %s already exists'%filename
	else:
		break
		
#get file content(text)lines
all=[]
print "\nEnter lines('.' by itself to quit).\n"

#loop until user terminates input
while True:
	entry=raw_input('>')
	if entry=='.':
		break
	else:
		all.append(entry)

#write lines to file with proper line-ending
fobj=open(filename, 'w')
fobj.writelines('%s%s'%(x, ls)for x in all)
fobj.close()
print 'Done'