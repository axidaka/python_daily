
print "*******************lie biao**************************"
shoplist = ['apple', 'mango', 'banana', 'paper']

print 'I have', len(shoplist), 'items to buy'

print 'These items are:'
for item in shoplist:
    print item

print 'I also have to buy rice'
shoplist.append('rice')
print 'My shopping list is now', shoplist

print 'I will sort my list now'
shoplist.sort()
print 'Sorted shopping list is now', shoplist

print 'The first item I will buy is', shoplist[0]
olditem = shoplist[0]
del shoplist[0]
print 'I bought the', olditem
print 'My shopping list is now', shoplist

print "\n******************yuan zu*************************"

zoo = ('wolf', 'elephant', 'penguin')
print 'Number of animals in the zoo is', len(zoo)

new_zoo = ('monkey', 'dolphin', zoo)
print 'Numbers of animals in the new zoo is ', len(new_zoo)
print 'All animals in new zoo are', new_zoo
print 'Added animals in new zoo are', new_zoo[0:2]
print 'Animals also brought from old zoo are', new_zoo[2]
print 'Last animal brought from old zoo is', new_zoo[2][2]

print '\n******************print with yuan zu************************'

age = 22
name = 'Swaroop'

print '%s is %d years old' % (name, age)
print 'Why is %s playing with that python' % name

print '\n*******************dictionary****************************'
ab = {'Swaroop': 'swaroopch@byteofpython.info',
      'Larry': 'larry@wall.org',
      'Matsumoto': 'matz@ruby-lang.org',
      'Spammer': 'spammer@hotmalil.com'}
print "Swaroop's address is %s" % ab['Swaroop']

# adding a key/value pair
ab['Guido'] = 'guido@python.org'

# Deleting a key/value pair
del ab['Spammer']

print '\n There are %d contacts in the address-book\n' % len(ab)
for name, address in ab.items():
    print 'Contact %s at %s' % (name, address)

if 'Guido' in ab:  # or ab.has_key('Guido')
    print "\nGuido's address is %s" % ab['Guido']

print '\n********************xu lie********************************'

sequence = ['apple', 'manago', 'carrot', 'banana']

print "All item is", sequence
print 'Item 0 is', sequence[0]
print 'Item 1 is', sequence[1]
print 'Item 2 is', sequence[2]
print 'Item 3 is', sequence[3]
print 'Item -1 is', sequence[-1]
print 'Item -2 is', sequence[-2]

print 'Item 1 to 3 is', sequence[1:3]
print 'Item 2 to end is', sequence[2:]
print 'Item 1 to 1- is', sequence[1:-1]
print 'Item start to end is', sequence[:]

print '\n********************reference*******************************'
print 'Simple Assignment'
myShoppList = ['apple', 'manago', 'carrot', 'banana']
# refObject is just another name pointing to the same object
refObjcet = myShoppList

print 'Before del myShoppList[0]:', myShoppList
del myShoppList[0]
print 'After del myShoppList[0]:', myShoppList
print 'After del myShoppList[0],refObjcet:', refObjcet

del refObjcet[0]
print 'After del refObjcet[0],myShoppList:', myShoppList
print 'After del refObjcet[0],refObjcet:', refObjcet

print 'Copy by making a full slice'
copyObject = myShoppList[:]  # make a copy by doing a full slice
del myShoppList[0]
print 'myShoppList:', myShoppList
print 'copyObject:', copyObject
