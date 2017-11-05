#coding:utf-8
CODEC='utf-8'
FILE='unicode.txt'

hello_out=u'Hello world\n世界，你好\n'
bytes_out=hello_out.encode(CODEC)
f=open(FILE, 'w')
f.write(bytes_out)
f.close()

f=open(FILE, 'r')
byte_in=f.read()
f.close()
hello_in=byte_in.decode(CODEC)
print hello_in

