# -*- coding: utf-8 -*-

import os
import sys

path_root= os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, path_root)

from practice import DnfboxFileZip


if __name__ == "__main__":
   #测试反复启动DNF盒子
   #auto_test.runTest.run_dnfbox();
   DnfboxFileZip.ZipDNFUpdateFiles()
