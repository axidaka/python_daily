#!/usr/bin/env python
#coding=utf-8
author =  "zhqs"

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import time
import urllib, urllib2, urlparse
import os, sys
import socket
import logging
import threading


class SpiderOnePieceChapters(object):
    """爬取海贼王每一集的名称"""

    def __init__(self, baseUrl, htmlQueue, savepath):
        super(SpiderOnePieceChapters, self).__init__()
        self.urlQueue = htmlQueue
        self._logger = logging.getLogger(__name__)
        self.count = 0
        self.urlQueue.reverse()
        self.titlelist = []
        self.dictTitle2ImgUrl = {}   #标题映射图片url
        self.savepath = savepath
        if not os.path.exists(self.savepath):
            os.makedirs(self.savepath)

    def run(self, nloop):
        while self.urlQueue:
            # self._logger.info('Thread:%d', nloop)
            url = self.urlQueue.pop()
            self.downloadPic(url)

    def downloadPic(self, url):
        html = self.getHtml(url)
        if not html:
            return

        # 先获取<ul >***</ul>的***内容, 结果为<li><a></a></li>
        self.reg = r"<ul .*?>(.*?)</ul>"
        OnePiecelist = re.findall(self.reg, self.getHtml(url), re.S|re.M)
        for  onepiece in OnePiecelist:

            if type(onepiece).__name__ != "unicode":
                onepiece = unicode(onepiece, "gbk")

            # < li >
            # < a
            # href = "http://www.narutom.com/onepiece/video/31364.html"
            # title = "海贼王第758集「日间之王 犬岚公爵登场!」"
            # target = "_blank" >
            # < img
            # alt = "海贼王第758集「日间之王 犬岚公爵登场!」"
            # src = "http://www.narutom.com/d/file/onepiece/video/2016-10-02/f8a87918b258efebe3130b69114befd0.jpg" >
            # < / a >
            # < a
            # href = "http://www.narutom.com/onepiece/video/31364.html"
            # title = "海贼王第758集「日间之王 犬岚公爵登场!」"
            # target = "_blank" > 海贼王第758集「日间之王
            # 犬岚公爵登场!」
            # < / a >
            # < / li >

            # 再获取<a>***</a>的***内容
            self.reg = r'<a.*?target="_blank">(.*?)<\/a>'
            alist = re.findall(self.reg, onepiece, re.S | re.M)
            for item in alist:
                if type(item).__name__ != "unicode":
                    item = unicode(item, "gbk")

                if item.find("<img") != -1:
                    # < img
                    # alt = "海贼王第779集「凯多再次袭来 威胁重重的极恶时代!」"
                    # src = "http://www.narutom.com/d/file/onepiece/video/2017-03-05/71a0946f5a4f2d6b19ffbd893546cec0.jpg"
                    # >
                    # r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
                    title = re.findall('(?<=alt=\").+?(?=\")', item, re.S | re.M).pop()
                    imgurl = re.findall('(?<=src=\").+?(?=\")', item, re.S | re.M).pop()
                    (tmp,extension) = os.path.splitext(imgurl)
                    title = title.replace(' ', '')
                    title = title.replace('海贼王', '')
                    title = title.replace('第', '')
                    title += extension

                    if imgurl.find('ttp://www.narutom.com/') == -1:
                        imgurl = 'http://www.narutom.com/' + imgurl

                    self.dictTitle2ImgUrl[title] = imgurl

                    # 直接下载图片
                    jpgname = title
                    jpgpath = os.path.join(self.savepath, jpgname)

                    if not os.path.exists(jpgpath):
                        try:
                            # urllib2.urlopen(imgurl)
                            urllib.urlretrieve(imgurl, jpgpath)
                            print imgurl
                        except urllib2.HTTPError, e:
                            self._logger.exception('urllib2.urlopen HTTPError')
                        except urllib.ContentTooShortError, e:
                            self._logger.exception("urlib ContentTooShortError")
                        except IOError, e:
                            self._logger.exception("IOError")
                    continue
                # 特别的集名为 <font color="#DD22DD">海贼王15周年特别篇「3D2Y跨越艾斯之死!」</font>
                if item.find("<font") != -1:
                    item = re.findall("<font.*?>(.*?)</font>", item, re.S | re.M).pop()
                    print "特殊：：：：%s" % (item)
                self.titlelist.append(item)
                # self._logger.debug('%s\n', item)



        # for (title, url) in self.dictTitle2ImgUrl.items():
        #     jpgname = title + '.jpg'
        #     jpgpath = os.path.join(self.savepath, jpgname)
        #
        #     if not os.path.exists(jpgpath):
        #         try:
        #             urllib2.urlopen(url)
        #             urllib.urlretrieve(url, jpgpath)
        #             # self.count += 1
        #             # print 'count:', self.count
        #             print url
        #         except urllib2.HTTPError, e:
        #             self._logger.exception('urllib2.urlopen except')
        #         except urllib.ContentTooShortError, e:
        #             self._logger.exception('urllib2.urlretrieve')

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


def SpiderOnePieceChapters_Test():
    htmlQueue = []

    # 火影忍者中文网
    baseUrl = u"http://www.narutom.com/onepiece/video/"
    htmlQueue.append(baseUrl)
    for i in range(2, 41):
        newurl = "%sindex_%d.html" % (baseUrl, i)
        htmlQueue.append(newurl)

    spiderobj = SpiderOnePieceChapters(baseUrl.encode('utf-8'), htmlQueue, './Onepiece/')
    # spiderobj.run(1)

    threads = []
    for i in range(0, 9):
        threadobj = threading.Thread(target=threading_loop, args=(i, spiderobj))
        threads.append(threadobj)

    for i in range(0, 9):
        threads[i].start()

    for i in range(0, 9):
        threads[i].join()

    spiderobj.titlelist.reverse()
    for item in spiderobj.titlelist:
        # print item ,"\n"
        spiderobj._logger.debug("%s", item)

if __name__ == '__main__':
    log_file = os.path.realpath(sys.argv[0])[0:-3] + ".log"
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        filename=log_file,
                        filemode='w')
    SpiderOnePieceChapters_Test()