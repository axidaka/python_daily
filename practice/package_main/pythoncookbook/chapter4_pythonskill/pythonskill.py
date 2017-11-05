# coding:utf-8


def list_comprehension():
    """
    列表推导、生成器
    :return:
    """

    # 通过列表推导 构建新列表
    list1 = [x for x in range(10)]
    print list1

    list2 = [x for x in range(10) if x%2 == 0]
    print list2

    list3 = [x+1 for x in range(10) if x%2 != 0]
    print list3

    # 通过列表推导 修改 列表
    list1[:] = [min(x, 2) for x in list1]
    print list1

def list_get(L, i, v = None):
    """
    根据索引i获取L中元素, i不是有效索引返回默认值v
    :param L: 列表
    :param i: 索引
    :param v: 默认值
    :return: 元素
    """
    if -len(L) <= i < len(L): return L[i]
    else: return  v

def traver_seq(seq):
    """
    循环访问序列中的元素和索引
    :param seq: 可迭代序列
    :return:
    """
    for index, value in enumerate(seq):
        if isinstance(seq, dict):
            print index, ':', value, ':', seq[value]
        else:
            print index, ':', value

def create_listoflist():
    """
    在无须共享引用的条件下创建列表的列表（其实就是多维矩阵)
    :return:
    """
    # 方式1 会导致修改其中一个元素，其他元素也会改变
    multi1 = [[0]*5]*3
    print multi1
    multi1[0][0] = 1
    print 'After change multi1[0][0] = 1>>', multi1

    # 使用列表推导创建
    multi2 = [[0 for col in range(3)] for row in range(5)]
    print multi2
    multi2[0][0] = 1
    print 'After change multi2[0][0] = 1>>', multi2


def list_or_tuple(x):
    return isinstance(x, (list, tuple))

def flatten(sequence, to_expand = list_or_tuple):
    """
    用于展开一个嵌套序列的生成器
    :param sequence: 序列
    :param to_expand: 判断序列的函数，可替换， 默认是判断当前是否为 列表或者元组
    :return:
    """
    for item in sequence:
        if to_expand(item):
            for subitem in flatten(item, to_expand):
                yield subitem
        else:
            yield  item

def column_swap_row(sequence):
    """
    二维矩阵行列变换
    :param sequence: 序列每一项的长度都需要相同
    :return:
    """
    #方法1
    #return  [[sequence[row][col] for row in range(len(sequence))] for col in range(len(sequence[0]))]

    #方法2
    return [[row[col] for row in sequence]for col in range(len(sequence[0]))]

def add_word(theIndex, word, pagenumber):
    """
    给字典添加一条条目
    :param theIndex: 字典
    :param word: 单词
    :param pagenumber:单词所在的页数列表
    :return:
    """
    #方法1,简洁
    theIndex.setdefault(word, []).append(pagenumber)

    #方法2,易懂
    # if word in theIndex:
    #     theIndex[word].append(pagenumber)
    # else:
    #     theIndex[word] = [pagenumber]

    #方法3
    # try:
    #     theIndex[word].append(pagenumber)
    # except KeyError:
    #     theIndex[word] = [pagenumber]


def pairwise(iterable):
    """
    从可迭代对象获取多个数对， 生成器
    :param iterable:
    :return:
    """
    it_next = iter(iterable).next  # next 为方法， it_next为本地名称
    while True:
        yield  it_next(), it_next()

def dictFromList(keysAndValues):
    """
    将列表元素交替作为键和值来创建字典
    :param keysAndValues: 列表
    :return:
    """
    #方法1， 使用切片函数和zip
    #return dict(zip(keysAndValues[::2], keysAndValues[1::2]))

    #方法2，使用生成器创建Pair对
    return dict(pairwise(keysAndValues))

def sub_dict(somedict, somekeys, default=None):
    """
    获取字典的一个子集
    :param somedict:字典
    :param somekeys:键值集合
    :param default:
    :return:
    """
    #如果想从原字典中删除， 可以使用pop
    return dict((key, somedict.get(key, default)) for key in somekeys)

def dict_union_inter(dictobja, dictobjb):
    """
    字典的并集 交集
    """
    # 通过dict构造函数 列表推导
    union = dict(dictobja, **dictobjb)
    inter = dict.fromkeys([x for x in dictobja if x in dictobjb])
    print union, inter

    # 通过转化成集合 使用 | &
    seta = set(dictobja)
    setb = set(dictobjb)
    union = seta | setb
    inter = seta & setb
    print union, inter

def printf(format, *args):
    """
    实现C风格printf
    """
    import sys
    sys.stdout.write(format % args)

def returns(t, f, *a, **k):
    """
    正常情况下返回[f(*a, **k)], 若有异常返回[]
    """
    try:
        return [f(*a, **k)]
    except t:
        return []

def main():
    list_comprehension()

    list1 = [x for x in range(10)]
    print 'list1:', list1
    print 'list_get:10:', list_get(list1, 10)
    print 'list_get:-5:', list_get(list1, -5)
    print 'list_get:-100:',list_get(list1, -100, 100)

    traver_seq(list1)
    traver_seq(dict(a=1, b=3, c = 5))

    create_listoflist()

    for x in flatten([ [x for x in range(10)] for col in range(10)]):
        print x

    print column_swap_row([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])

    print dictFromList([x for x in range(10)])

    print sub_dict(dictFromList([x for x in range(10)]), (1, 2, 3), 5555)

    print dict_union_inter(dict.fromkeys(range(100)), dict.fromkeys(range(50, 150)))

    printf("Use Python define %s", "printf")

    except_test = list((1, 'a', ' ', 33, 55, 'lll', 33344))
    print [x for fobj in except_test for x in returns(ValueError, float, fobj)]

if __name__ == "__main__":
    main()