# coding:utf-8


from random import randint


def randGen(aList):
    '从序列返回一个随机元素的随机迭代器'
    while len(aList) > 0:
        yield aList.pop(randint(1, len(aList)) - 1)


def counter(start_at=0):
    count = start_at

    while True:
        val = (yield count)
        if val is not None:
            count = val
        else:
            count += 1

if __name__ == "__main__":
    for item in randGen(['Tecent', 'Alibaba', 'Baidu']):
        print item

    for item in randGen(range(1, 11)):
        print item

    for item in counter(5):
        print item
