# -*- coding:utf-8 -*-

def sortedDictValues(adict):
    """
    对字典排序：实际目的是将字典中的键构成的序列排序
    :param adict:
    :return:
    """
    try:
        if isinstance(adict, dict):
            keys = adict.keys()
            keys.sort()
            return map(adict.get, keys)
    except:
        raise TypeError("adict Not a dict type")

def case_insensitive_sort(string_list):
    """
    不区分大小写对字符串列表排序
    """
    # 方法1 使用 dsu模式
    # temp_list = [(x.lower(), x) for x in string_list] #decorate
    # temp_list.sort()                                  #sort
    # return [x[1] for x in temp_list]                  #undecorate

    #方法2
    def mycompare(a, b ): return cmp(a.lower(), b.lower())
    return  sorted(string_list, cmp=mycompare)

def main():
    print sortedDictValues(dict(a=1, c=2, f=3, d=4, e = 5))

    print case_insensitive_sort(['a', 'c', 'd', 'f', 'e', 'b', 'g'])

if __name__ == "__main__":
    main()