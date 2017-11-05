# coding:utf-8

import os
import zipfile
import tarfile
import types
import tempfile
import win32api

def dellinebreak(line):
    '''删除换行符'''
    print line.rstrip('\n')
    # 整个文件处理可以 fileobject.read().splitlines() or file_object.read().split('\n')


def readfile(filename, handlewith_line):
    '''读取文件在不确定文本文件会用什么样的换行符，可以使用rU模式指定通用换行符转化，各种平台下的换行符将被映射成'\n' '''
    file_object = open(filename, 'rU')
    try:
        for line in file_object:  # 使用迭代方式在处理大文件时避免消耗太多内存
            handlewith_line(line)
    finally:
        file_object.close()


def replaceword_infile(srcfile, srcword, dstfile, dstword):
    '''搜索和替换文件的文本'''
    srcfile_object = open(srcfile)
    dstfile_object = None

    if len(dstfile) == 0:
        import sys
        dstfile_object = sys.stdout
    else:
        dstfile_object = open(dstfile, 'w')

    try:
        dstfile_object.write(srcfile_object.read().replace(srcword, dstword))
    finally:
        srcfile_object.close()
        dstfile_object.close()


def getspecifyline_infile(filename, beginline, endline=None):
    '''从文件获取指定的行'''
    if beginline < 1:
        return ''
    if not endline:
        endline = beginline

    import linecache
    retline = str()
    while (beginline <= endline):
        retline += linecache.getline(filename, beginline)
        beginline += 1

    return retline


def getfile_linecounts(filename):
    '''获取文件行数'''
    file_object = open(filename)
    try:
        return len(file_object.readlines())  # 对于大文件来说可能很慢,耗内存

        # for count, line in enumerate(file_object): #大文件，可采取循环计数
        # pass
        # count += 1
    finally:
        file_object.close()


def words_of_file(filepath, line_to_words=str.split):
    '''将迭代文件操作封装成生成器，复用'''
    file_object = open(filepath)

    try:
        for line in file_object:
            for word in line_to_words(line):
                yield word
    finally:
        file_object.close()


def unzip_file(zipfilepath, unzipdir):
    '''解压文件'''
    if not os.path.exists(unzipdir):
        os.mkdir(unzipdir)

    zfobj = None

    try:
        zfobj = zipfile.ZipFile(zipfilepath)
        zfobj.extractall(unzipdir)

    finally:
        zfobj.close()


def zip_dir(dirname, zipfilepath):
    '''压缩文件'''
    filelist = []

    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for dirpath, dirnames, filenames in os.walk(dirname):
            for item in filenames:
                filelist.append(os.path.join(dirpath, item))

    if os.path.exists(zipfilepath):
        os.remove(zipfilepath)

    zfobj = zipfile.ZipFile(zipfilepath, 'w', zipfile.ZIP_DEFLATED)
    for abspath in filelist:
        print 'adspath', abspath
        archive = abspath[len(dirname):]
        zfobj.write(abspath, archive)
    zfobj.close()


def make_tar(folder_to_backup, dest_folder, compression='bz2'):
    '''文件归档到压缩的tar文件'''
    if compression:
        dest_ext = '.' + compression
    else:
        dest_ext = ''

    arcname = os.path.basename(folder_to_backup)
    dest_name = '%s.tar%s' % (arcname, dest_ext)
    dest_path = os.path.join(dest_folder, dest_name)

    if os.path.exists(dest_path):
        os.remove(dest_path)
    if compression:
        dest_cmp = ':' + compression
    else:
        dest_cmp = ''
    out = tarfile.TarFile.open(dest_path, 'w' + dest_cmp)
    out.add(folder_to_backup, arcname)
    out.close()
    return dest_path

CHUNK_SIZE = 16 * 1024


def adapt_filelike(file_object):
    '''将类文件对象适配为真实文件对象，使用完后需要close'''
    if isinstance(file_object, file):
        return file_object

    tmpfileobject = tempfile.TemporaryFile()
    while True:
        data = file_object.read(CHUNK_SIZE)
        if not data:
            break
        tmpfileobject.write(data)

    file_object.close()
    tmpfileobject.seek(0)
    return tmpfileobject


def all_files(root, pattern='*', single_level=False, yield_folders=False):
    '''根据文件格式遍历目录树'''
    patternlst = pattern.split(';')

    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)

        files.sort()

        import fnmatch

        for name in files:
            for patternitem in patternlst:
                if fnmatch.fnmatch(name, patternitem):
                    yield os.path.join(path, name)
                    break

        if single_level:
            break


def swapextension(dir, before, after):
    '''修改指定类型的文件扩展名'''
    if before[:1] != '.':
        before = '.' + before

    if after[:1] != '.':
        after = '.' + after

    import os.path

    for path, subdirs, files in os.walk(dir):
        for oldfile in files:
            (name, extension) = os.path.splitext(oldfile)
            if extension == before:
                oldfilepath = os.path.join(path, oldfile)
                newfilepath = os.path.join(path, (name + after))
                os.rename(oldfilepath, newfilepath)


def search_file_bypattern(patterns, search_path, pathsep=os.pathsep):
    '''给定搜索路径，找出所有满足匹配条件的文件,不会查找目录下的子目录'''
    import glob
    patternlst = patterns.split(';')
    for itempattern in patternlst:
        for path in search_path.split(pathsep):
            for match in glob.glob(os.path.join(path, itempattern)):
                yield match


def addsyspath(new_path):
    '''给Python的sys.path增加目录'''

    import sys
    import os

    if not os.path.exists(new_path):
        return -1

    # 将路径标准化，windows是大小写不敏感的，所以若确定在window下，将其转化成小写
    new_path = os.path.abspath(new_path)

    if sys.platform == 'win32':
        new_path = new_path.lower()

    # 检查所有的路径
    for x in sys.path:
        x = os.path.abspath(x)
        if sys.platform == 'win32':
            x = x.lower()
        if new_path in (x, x + os.sep):
            return 0
    sys.path.append(new_path)
    return 1

def getFileVersion(file_name):
    '''使用win32api 获取文件版本号'''
    if (os.path.isfile(filename)):
        info = win32api.GetFileVersionInfo()
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        version = '%d.%d.%d.%04d' % (win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls))
        return version
    else:
        return ""

'''跨平台读取无缓存的字符'''
try:
    from msvcrt import getch
except ImportError:
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
if __name__ == '__main__':
    # readfile(__file__, dellinebreak)
    # replaceword_infile(__file__, 'utf-8', '', 'gbk')
    # print getspecifyline_infile(__file__, 3)
    # print getfile_linecounts('C:\\result.txt')
    # for word in words_of_file(__file__):
    #     print word
    # unzip_file(r'C:\Python27\test.zip', r'C:\python27\unzipTest')
    # zip_dir(r"G:\xiazai", r'G:\test.zip')
    # print make_tar(r'G:\xiazai', r'G:')
    # import urllib2
    # filelike = urllib2.urlopen('http://huya.com')
    # realfile = adapt_filelike(filelike)
    # print realfile.name
    # print realfile.read()
    # realfile.close()
    # for path1 in all_files(r'D:\Program Files (x86)\Microsoft Visual Studio 9.0', '*.exe;*.htm'):
    #     print path1
    #swapextension(r'G:\xiazai', 'txt', 'mytxt')
    #swapextension(r'G:\xiazai', 'mytxt', 'txt')
    # print list(search_file_bypattern('*.txt;*.xml',
    # r'G:\test;G:\test\subdir1'))
    # new_path = r'E:\云U盘\19729989\Learn NewKnowledge\Python'
    # import os
    # for root, subdirs, files in os.walk(new_path.decode('utf-8').encode('gbk')):
    #     for itemsubdir in subdirs:
    #         print 'new_path:', os.path.join(root, itemsubdir)
    #         addsyspath(os.path.join(root, itemsubdir))
    ch = getch()
    print 'you enter char:',ch