dict1=dict(x=1,y=2,z=3)
print dict1
	
for (k,v) in dict1.items():
	print '%s:%s'%(k,v)	
	
for eachkey in sorted(dict1):
	print 'key:%s value:%s'%(eachkey, dict1[eachkey])
	
for k,v in dict1.iteritems():
	print k, v
	
for k in dict1.iterkeys():
	print k, dict1[k]
	
db={}

def newuser():
	prompt='login desired:'
	while True:
		name=raw_input(prompt)
		if db.has_key(name):
			prompt='name taken, try another:'
			continue
		else:
			break
	pwd=raw_input('passwd:')
	db[name]=pwd

def olduser():
	name=raw_input('login:')
	pwd=raw_input('passwd:')
	passwd=db.get(name)
	if pwd==passwd:
		print 'welcome back',name
	else:
		print 'login incorrect0'
	
def showmenu():
	prompt='''
	(N)ew User Login
	(E)xisting User Login
	(Q)uit
	Enter choice:
	'''

	done=False

	while not done:
		chosen=False
		while not chosen:
			try:
				choice=raw_input(prompt).strip()[0].lower()
			except(EOFError, KeyboardInterupt):
				choice='q'
			print '\n You picked:[%s]'%choice
			
			if choice not in 'neq':
				print 'invalid option, try again'
			else:
				chosen=True
				done=True
	newuser()
	olduser()

import time
if __name__=='__main__':
	#showmenu()
	fxbegin=time.time()
	for n in xrange(1000000):
		print n
	fxend=time.time()
	
	fbegin=time.time()
	for n in range(1000000):
		print n
	fend=time.time()
	print 'Xrange:%f'%(fxend - fxbegin)
	print 'range:%f'%(fend - fbegin)