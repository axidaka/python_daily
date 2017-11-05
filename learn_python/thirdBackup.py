#coding:utf-8
import os
import time
import sys

def BackupDir(src=r'F:\Learn NewKnowledge\Python\*', target=r'F:\Learn NewKnowledge\Backup'):
	
	#1.The files and dir to be backed up are specified in a list
	source=[src,]

	#2The backup must be stored in a main backup dir
	target_dir=target

	#3The files are backed up in to a zip file
	today=target_dir + os.sep + time.strftime("%Y-%m-%d")
	now=time.strftime("%H-%M-%S")

	#Take a comment from the user to create the name of the zip file
	comment=raw_input("Enter a comment->")
	if len(comment) ==0:
		taget_file=today + os.sep + now + '.zip'
	else:
		taget_file=today + os.sep + now + '_' + \
		comment.replace(' ','_') + '.zip'
		
	if not os.path.exists(today):
		os.mkdir(today)
		print 'Successfully created dir',today
		
	#4 zip command
	zip_command=r'HaoZipC a -tzip "%s" "%s"'% (taget_file,source[0])

	print zip_command
	#5 run
	if os.system(zip_command) == 0:
		print "Successfully backup to",taget_file
	else:
		print "Backup Falied"




def main():
	print 'commandline:',sys.argv
	
	if len(sys.argv)==1:
		BackupDir()
	elif len(sys.argv)==3:
		BackupDir(sys.argv[1],sys.argv[2])
	else:
		print 'Commandline is unvalid'
	
#end of main

if __name__ == '__main__':
	main()