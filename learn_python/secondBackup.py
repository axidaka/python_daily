import os
import time

#1.The files and dir to be backed up are specified in a list
source=[r"F:\Learn NewKnowledge\Python\*",]

#2The backup must be stored in a main backup dir
target_dir='F:\Learn NewKnowledge\Backup'

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

