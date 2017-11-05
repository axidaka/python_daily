# coding:utf-8

import os
import shutil
import hashlib

def fillfiletype(srcPath, dstPath, fileType):
    "读取目录所有文件，判断是否有后缀格式，否添加png,遍历+递归"
    if os.path.isdir(srcPath):
        listItems = os.listdir(srcPath)

    for item in listItems:
        itemSrcPath = os.path.join(srcPath, item)
        itemDstPath = os.path.join(dstPath, item)

    if os.path.isdir(itemSrcPath):  # 递归调用
        fillfiletype(itemSrcPath, itemDstPath, fileType)
    elif os.path.isfile(itemSrcPath):
        (filename, filetype) = os.path.splitext(item)

    if len(filetype) == 0:  # 找到符合条件的文件
        print "Right File", itemSrcPath
        # 为dst创建目录，判断文件是否存在
        if not os.path.exists(dstPath):  # 传入的dstPath可能是没有提前创建的
            os.makedirs(dstPath)
            print 'Create Dir:', dstPath

    itemDstPath += fileType
    print itemDstPath
    if not os.path.exists(itemDstPath):
        shutil.copy(itemSrcPath, itemDstPath)
    else:
        print srcPath, 'is invalid dir'


def calcMD5(filepath):
    f = open(filepath, 'rb')
    md5obj = hashlib.md5()
    md5obj.update(f.read())
    hashval = md5obj.hexdigest()
    f.close()
    return hashval


class copyandsortfiletype(object):

    '将源目录下文件按照格式分类到目标目录'

    def __init__(self, srcPath, dstPath):
        self.srcPath = srcPath
        self.dstPath = dstPath
        self.dictdir2hashlst = dict()

    def scanfdstpath(self):
        '扫描目标目录下文件的hash值'
        print '正在扫描目录:', self.dstPath
        if os.path.isdir(self.dstPath):

            listitems = os.listdir(self.dstPath)
            for item in listitems:  # 遍历子目录

                fullpath = os.path.join(self.dstPath, item)
                if os.path.isdir(fullpath):

                    setMD5s = set()
                    listfiles = os.listdir(fullpath)
                    for fileitem in listfiles:  # 遍历文件
                        filepath = os.path.join(fullpath, fileitem)
                        tmpMd5 = calcMD5(filepath)
                        if tmpMd5 not in setMD5s:
                            setMD5s.add(tmpMd5)
                        else:
                            os.remove(filepath)
                    # 将该目录的所有文件的MD5列表保存到字典
                    self.dictdir2hashlst[item] = setMD5s

    def isfilerepeat(self, filetype, filepath):
        '判断文件在目标目录是否重复'
        brepeat = False
        tmpMd5 = calcMD5(filepath)

        if self.dictdir2hashlst.has_key(filetype):
            if tmpMd5 not in self.dictdir2hashlst[filetype]:
                self.dictdir2hashlst[filetype].add(tmpMd5)
            else:
                brepeat = True
                print 'repeat:', filepath
        else:
            setMD5s = set()
            setMD5s.add(tmpMd5)
            self.dictdir2hashlst[filetype] = setMD5s

        return brepeat

    def copy(self):
        print '执行拷贝.....'
        if os.path.isdir(self.srcPath):

            for curdir, subdirs, files in os.walk(self.srcPath):

                # 先处理文件
                for fileitem in files:
                    (filename, filetype) = os.path.splitext(fileitem)

                    if len(filetype) != 0:
                        filetype = filetype[1:]
                        newdir = os.path.join(self.dstPath, filetype)
                        newfile = os.path.join(newdir, fileitem)
                        oldfile = os.path.join(curdir, fileitem)

                        if not os.path.exists(newdir):
                            os.makedirs(newdir)

                        if not os.path.exists(newfile):
                            if not self.isfilerepeat(filetype, oldfile):
                                shutil.copy(oldfile, newfile)
        else:
            print self.srcPath, 'is invalid dir'

    def run(self):
        self.scanfdstpath()
        # for (key, value) in self.dictdir2hashlst.items():
        #     print 'key:', key, value
        self.copy()


import logging
import distutils.dir_util
import ConfigParser
import sys
import urllib2
import tarfile

REPO_URL_ROOT = "http://repo.yypm.com/dwintegrate"


class GetDependLibs(object):
    """根据配置文件获取依赖库"""

    def __init__(self, depend_dir, dependslist_cfg):
        super(GetDependLibs, self).__init__()
        self.depend_dir = depend_dir
        self.dependslist_cfg = dependslist_cfg
        self._logger = logging.getLogger(__name__)

    def parseDependlist(self):

        # 创建目录
        distutils.dir_util.mkpath(self.depend_dir)

        # 创建解析配置文件的对象
        dependscfg = ConfigParser.SafeConfigParser()
        # dependscfg 必须支持大写的key
        dependscfg.optionxform = str
        dependscfg.read(self.dependslist_cfg)

        for repo_section in dependscfg.sections():
            self._logger.debug("repo_secction:%s", repo_section)

            allLib = {}

            for libname, libversion in dependscfg.items(repo_section):
                allLib[libname] = DownLoadLib(
                    repo_section, libname, libversion, self.depend_dir)

            for value in allLib.itervalues():
                value.runDownload()


class DownLoadLib(object):
    """下载依赖库"""

    def __init__(self, section, libname, libversion, depend_dir):
        super(DownLoadLib, self).__init__()
        self._section = section
        self._libname = libname
        self._libversion = libversion
        self._depend_dir = depend_dir
        self._logger = logging.getLogger(__name__)

        self._repo_path = "%s/%s/%s/%s/" % (REPO_URL_ROOT,
                                            self._section,
                                            self._libname,
                                            self._libversion)

        self._local_path = os.path.join(self._depend_dir,
                                        self._section,
                                        self._libname)

        self._logger.debug('''dependlib path:
            repo: %s
            local: %s
            ''' % (self._repo_path, self._local_path))

    def runDownload(self):
        self._logger.info('dependlib[%s.%s] start',
                          self._libname, self._libversion)

        if os.path.exists(self._local_path):
            distutils.dir_util.remove_tree(self._local_path)

        distutils.dir_util.mkpath(self._local_path)

        file_list = [
            'bin.tar.gz',
            'dev.tar.gz',
            'pdb.tar.gz', ]

        for fileitem in file_list:
            self._download(fileitem, self._local_path)

        self._logger.info('dependlib[%s.%s] finish',
                          self._libname, self._libversion)

    def _download(self, fileitem, dest_dir):
        url = "%s/%s" % (self._repo_path, fileitem)
        destfile = os.path.join(dest_dir, fileitem)

        ret = None
        try:
            ret = urllib2.urlopen(url, timeout=30)
        except urllib2.HTTPError as e:
            # if report_404:
            #     raise Exception('download fail[%s]'% url)
            # else:
            self._logger.debug('[%s] is not exist', url)

        if ret != None:
            with open(destfile, 'wb') as w:
                w.write(ret.read())

            self._logger.info('download success [%s]', url)

        self._unpack_alltar()

    def _unpack_alltar(self):
        for f in os.listdir(self._local_path):
            if f.endswith('.tar.gz'):
                gz_path = os.path.join(self._local_path, f)
                tarobj = tarfile.open(gz_path, 'r:gz')
                tarobj.extractall(self._local_path)
                tarobj.close()


def GetDepend_Test():
    cwdpath = os.getcwd()
    depend_dir = cwdpath + '\depends'
    dependslist_cfg = cwdpath + '\depend.list'

    log_file = os.path.realpath(sys.argv[0])[0:-3] + '.log'
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        filename=log_file,
                        filemode='w')

    testobj = GetDependLibs(depend_dir, dependslist_cfg)
    testobj.parseDependlist()


import re
import time
import urllib


class SpiderPicOline(object):
    """网页爬取图片"""

    def __init__(self, baseUrl, pagecount, dstpath):
        super(SpiderPicOline, self).__init__()
        self.urlQueue = [baseUrl]
        self.pagecount = pagecount
        self.dstpath = dstpath

        for i in range(2, self.pagecount):
            newurl = "%s&pager_offset=%d"%(baseUrl, i)
            print 'newUrl:', newurl
            self.urlQueue.append(newurl)

    def run(self):
        while  self.urlQueue:
            url = self.urlQueue.pop()
            self.downloadPic(url)

    def downloadPic(self, url):
        #reg = r'href="(.+?\.jpg)" target'
        reg = r'src="(.+?\.jpg)"'  
        imgre = re.compile(reg)
        imglist = re.findall(imgre, self.getHtml(url))
        #print 'imglist', imglist

        # 定义文件夹名称
        t = time.localtime(time.time())
        foldername = str(t.__getattribute__("tm_year")) + "-" + str(
            t.__getattribute__("tm_mon")) + "-" + str(t.__getattribute__("tm_mday"))
        picpath = os.path.join(self.dstpath, foldername)

        if not os.path.exists(picpath):
            os.makedirs(picpath)

        for imgurl in imglist:
            print 'img:', imgurl
            jpgname = os.path.basename(imgurl)
            jpgpath = os.path.join(picpath, jpgname)
            if not os.path.exists(jpgpath):
                urllib.urlretrieve(imgurl, jpgpath)


    def getHtml(self, url):
        """下载整个网页html内容"""
        headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
        req = urllib2.Request(url, headers=headers)
        page = urllib2.urlopen(req)
        html = page.read()
        return html


def SpiderPic_Test():
    url = u"http://www.dbmeinv.com/dbgroup/show.htm?"
    #url = u"http://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gbk&word=%B8%DF%C7%E5%B1%DA%D6%BD&&fr=ala&oriquery=%E9%AB%98%E6%B8%85%E5%A3%81%E7%BA%B8&ala=1&alatpl=wallpaper&pos=3#z=&pn=&ic=0&st=-1&face=0&s=0&lm=-1&width=1920&height=1080"
    spiderobj = SpiderPicOline(url.encode('utf-8'), 50, r"G:\bizhi")
    spiderobj.run()

if __name__ == '__main__':
    # fillfiletype("D:\\png", "D:\\result", ".jpg")
    # sortfiletype(r"C:\Users\Administrator\AppData\Roaming\duowan\yy\cache\image", r"G:\test")

    dstpath = r"G:\test"
    copytest = copyandsortfiletype(r"C:\Users\Administrator\AppData\Roaming\duowan\yy\cache\image", dstpath.decode('utf-8').encode('gbk'))
    copytest.run()
    # GetDepend_Test()
    #SpiderPic_Test()
