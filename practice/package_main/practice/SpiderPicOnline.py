# coding:utf-8

import re
import time
import urllib, urllib2, urlparse
import os, sys
import socket
import logging
import threading


class SpiderPicOline(object):
    """网页爬取图片"""

    def __init__(self, baseUrl, htmlQueue, regPatter, dstpath):
        super(SpiderPicOline, self).__init__()
        self.dstpath = dstpath
        self.urlQueue = []
        self.reg = regPatter
        self._logger = logging.getLogger(__name__)
        self.count = 0

        for htmlname in htmlQueue:
            self.urlQueue.append(baseUrl + htmlname)

    def run(self, nloop):
        while self.urlQueue:
            self._logger.info('Thread:%d', nloop)
            url = self.urlQueue.pop()
            self.downloadPic(url)

    def downloadPic(self, url):
        # reg = r'href="(.+?\.jpg)" target'
        # reg = r'src="(.+?\.jpg)"'
        imgre = re.compile(self.reg)
        html = self.getHtml(url)
        if not html:
            return

        imglist = re.findall(imgre, self.getHtml(url))
        # print 'url:',url, '\nimglist', imglist

        # 定义文件夹名称
        urlParse = urlparse.urlparse(url)
        dom = urlParse[1]  # 域名
        urlpath = urlParse[2]
        picpath = os.path.join(self.dstpath, dom)

        for item in urlpath.split('/'):
            if item and (-1 == item.find('.htm')):
                picpath = os.path.join(picpath, item)

        if not os.path.exists(picpath):
            os.makedirs(picpath)

        for imgurl in imglist:
            jpgname = os.path.basename(imgurl)
            jpgpath = os.path.join(picpath, jpgname)

            # if imgurl.find('208x130') == -1:
            #    continue
            # imgurl = imgurl.replace('208x130', '1920x1080')

            # imgurl = 'http://www.th7.cn/' + imgurl

            # self._logger.debug('img %s', imgurl)
            if not os.path.exists(jpgpath):
                try:
                    urllib2.urlopen(imgurl)
                    urllib.urlretrieve(imgurl, jpgpath)
                    self.count += 1
                    print 'count:', self.count
                except urllib2.HTTPError, e:
                    # self._logger.exception('urllib2.urlopen except')
                    self._logger.error('imgurl fail: %s', imgurl)

        urllib.urlcleanup()

    def getHtml(self, url):
        """下载整个网页html内容"""
        headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
        req = urllib2.Request(url, headers=headers)
        try:
            page = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            # self._logger.exception('urlopen except')
            self.error('urlopen httpError: %s', url)
            return ""

        html = page.read()
        return html


def threading_loop(nloop, spiderobj):
    spiderobj.run(nloop)


def SpiderPic_Test():
    htmlQueue = []

    # 豆瓣妹子
    baseUrl = u"http://www.dbmeinv.com/dbgroup/show.htm?"
    htmlQueue.append(baseUrl)
    for i in range(2, 10000):
        newurl = "%s&pager_offset=%d" % (baseUrl, i)
        htmlQueue.append(newurl)

    # desk.zol.com壁纸
    # baseUrl = u"http://desk.zol.com.cn/meinv/1920x1080/"
    # for i in range(1, 1000):
    #     htmlname = 'hot_%d.html'% i
    #     htmlQueue.append(htmlname)

    # www.th7.cn
    # baseUrl = u"http://www.th7.cn/Design/photography/201408/"
    # htmlQueue.append('342070.shtml')
    # for i in range(2, 67):
    #     htmlname = '342070_%d.shtml'% i
    #     htmlQueue.append(htmlname)

    regPatter = r'src="(.+?\.jpg)"'

    spiderobj = SpiderPicOline(baseUrl.encode('utf-8'), htmlQueue, regPatter, r"G:\bizhi")
    # spiderobj.run(1)

    threads = []
    for i in range(0, 9):
        threadobj = threading.Thread(target=threading_loop, args=(i, spiderobj))
        threads.append(threadobj)

    for i in range(0, 9):
        threads[i].start()

    for i in range(0, 9):
        threads[i].join()


if __name__ == '__main__':
    log_file = os.path.realpath(sys.argv[0])[0:-3] + ".log"
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        filename=log_file,
                        filemode='w')

    SpiderPic_Test()
