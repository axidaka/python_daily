# coding:utf-8

import ConfigParser
import logging
import os
import sys

import fileprocess


class CollectPdb(object):
    """通过盒子版本号从构建系统目录收集当前版本dll exe的pdb文件"""

    def __init__(self, boxpath, dstpath):
        self.boxPath = boxpath
        self.dstPath = dstpath
        self.boxVersion = ""
        self._logger = logging.getLogger(__name__)

    def collect_pdbfiles(self):
        if self.detect_boxversion():
            print self.boxVersion
            self._logger.debug("boxVersion: %s", self.boxVersion)

        # 创建当前盒子版本pdb收集目录
        collectpath = os.path.join(self.dstPath, self.boxVersion)

        if os.path.exists(collectpath):
            os.mkdir(collectpath)

        pattern_list = "*.exe;*.dll"
        for file_item in fileprocess.search_file_bypattern(pattern_list, self.boxPath):
            file_version = fileprocess.get_fileversion(file_item)
            if 0 != len(file_version):
                print file_item, ':', file_version
            else:
                self._logger.error("get_fileversion failed: %s", file_item)

    def detect_boxversion(self):
        if os.path.isdir(self.boxPath):

            inifilePath = os.path.join(self.boxPath, "version.ini")
            if os.path.isfile(inifilePath):
                config = ConfigParser.ConfigParser()
                config.readfp(open(inifilePath))
                self.boxVersion = config.get("Version", "version")

                return len(self.boxVersion) != 0

        return False


if __name__ == '__main__':
    log_file = os.path.realpath(sys.argv[0])[0:-3] + ".log"
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        filename=log_file,
                        filemode='w')
    boxPath = r"D:\Program Files (x86)\多玩英雄联盟盒子"
    dstPath = r"G:\test"
    runObj = CollectPdb(boxPath.decode('utf-8').encode('gbk'), dstPath);
    runObj.collect_pdbfiles()
