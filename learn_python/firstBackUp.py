import os
import time

#1.The files and dir to be backed up are specified in a list
source=[r"F:\Learn NewKnowledge\Python\*",]

#2The backup must be stored in a main backup dir
target_dir='F:\Learn NewKnowledge\\'

#3The files are backed up in to a zip file
taget_file=target_dir+time.strftime("%Y-%m-%d-%H-%M-%S")+'.zip'

#4 zip command
zip_command=r'HaoZipC a -tzip "%s" "%s"'% (taget_file,source[0])

print zip_command
#5 run
if os.system(zip_command) == 0:
	print "Successfully backup to",taget_file
else:
	print "Backup Falied"

