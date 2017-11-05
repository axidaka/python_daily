# coding:utf-8

# 每次处理一个字符


def do_something_with(oneChar):
    return oneChar.upper(),

# 判断字符


def isStringLike(anObj):
    try:
        anObj.lower() + anObj + ''
    except:
        return False
    else:
        return True

# 合并字符串


def combineStrs(sequence):
    return ''.join(sequence)

# 按单词反转字符串（单词按照空格分割）


def reverseWords(strObject):
    return ' '.join(reversed(strObject.split()))


def test():
    '''每次处理一个字符'''
    teststring = 'abcdefghijklmn'
    result = [do_something_with(c) for c in teststring]
    print result

    teststring = 'abcdefghijklmn'
    result = map(do_something_with, teststring)
    print result

    print combineStrs(('ab', 'cdefg', 'hijk', 'lmn'))
    print combineStrs([str(i) for i in range(10)])

    print reverseWords('zheng qings song')
    print reverseWords('a b c d e f g')
if __name__ == '__main__':
    test()
    print isStringLike(1)
    print isStringLike('11')
