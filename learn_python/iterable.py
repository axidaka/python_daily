#coding:utf-8

import time

#低效率的访问文件
def GetLongestLine1():
	fxbegin=time.time()
	f=open("C:\\vcredist_x86.log", 'r')
	longest=0
	while True:
		linelen=len(f.readline().strip())
		if not linelen:
			break
		if linelen>longest:
			longest=linelen
	
	f.close()
	fxend=time.time()
	print 'time:',fxend-fxbegin
	return longest
	
def GetLongestLine2():
	fxbegin=time.time()
	f=open("C:\\vcredist_x86.log", 'r')
	longest=0
	alllines=f.readlines()
	f.close()
	for line in alllines:
		linelen=len(line.strip())
		if linelen>longest:
			longest=linelen
			
	fxend=time.time()
	print 'time:',fxend-fxbegin
	return longest
	
def GetLongestLine3():
	fxbegin=time.time()
	f=open("C:\\vcredist_x86.log", 'r')
	longest=0
	alllines=[x.strip() for x in f.readlines()]
	f.close()
	for line in alllines:
		linelen=len(line)
		if linelen>longest:
			longest=linelen
	
	fxend=time.time()
	print 'time:',fxend-fxbegin
	return longest

def GetLongestLine4():
	fxbegin=time.time()
	f=open("C:\\vcredist_x86.log", 'r')
	
	allLineLens=[len(x.strip())	for x in f]
	f.close()
	fxend=time.time()
	print 'time:',fxend-fxbegin
	return max(allLineLens)
	
def GetLongestLine5():
	fxbegin=time.time()
	longest=max(len(x.strip()) for x in open("C:\\vcredist_x86.log"))
	fxend=time.time()
	print 'time:',fxend-fxbegin
	return longest
	
if __name__ == '__main__':
	print GetLongestLine1()
	print GetLongestLine2()
	print GetLongestLine3()
	print GetLongestLine4()
	print GetLongestLine5()