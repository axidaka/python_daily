#!/usr/bin/python

# -- coding=utf-8 --

author = "zhqs"

import logging
import os
import shutil
import sys
import xml.dom.minidom
from xml.dom.minidom import parse

reload(sys)
sys.setdefaultencoding('utf-8')


class DaemonTemplate(object):

    def __init__(self, _src_dir, _xmlconf):
        self._logger = logging.getLogger(__name__)
        self.src_dir = _src_dir
        self.load_xmlconf(_xmlconf)

    def load_xmlconf(self, xmlconf):

        self._logger.debug("load xmlconf: %s", xmlconf)
        DOMTree = xml.dom.minidom.parse(xmlconf)
        JATS_Daemon_Template_conf = DOMTree.documentElement
        conf = JATS_Daemon_Template_conf.getElementsByTagName("conf")
        for item in conf:
            self.Rpm_Package = item.getElementsByTagName("Rpm_Package")[0].childNodes[0].data
            self.LogDir_Name = item.getElementsByTagName("LogDir_Name")[0].childNodes[0].data

            self.Executable_file = item.getElementsByTagName("Executable_file")[0].childNodes[0].data
            self.Monitor_File = item.getElementsByTagName("Monitor_File")[0].childNodes[0].data

            self.Proc_Num = item.getElementsByTagName("Proc_Num")[0].childNodes[0].data


    def create_jats_daemon_dir(self):
        dst_dir = os.getcwd() + os.sep + self.Rpm_Package + "_1"
        rmcmd = "rm -rf %s" % (dst_dir)
        os.system(rmcmd)

        shcmd = r"cp -r %s %s" % (self.src_dir, dst_dir)
        os.system(shcmd)

        # rename dir-----------begin-------------------------------------------------------------------------------------------------------
        #rename rpm_package
        os.chdir(dst_dir)
        os.chdir(r"./build_directory/data/bossapp")
        os.rename(r"unknown", self.Rpm_Package)
        self._logger.info("[./build_directory/data/bossapp] rename unknown->%s", self.Rpm_Package)

        #rename logdir 
        os.chdir(dst_dir)        
        os.chdir(r"./build_directory/data/bossapp/logs")
        os.rename(r"unknown_logdir", self.LogDir_Name)
        self._logger.info("[./build_directory/data/bossapp/logs] rename unknown->%s", self.LogDir_Name)
        # rename dir-----------end-------------------------------------------------------------------------------------------------------

        rmp_package_path = r"./build_directory/data/bossapp/" + self.Rpm_Package

        # modify file-----------begin-------------------------------------------------------------------------------------------------------
        # modify config.xml
        os.chdir(dst_dir)
        os.chdir(rmp_package_path + os.sep + "conf")

        shcmd = "sed -i 's/unknown_proc_num/" + self.Proc_Num + "/g' config.xml"
        os.system(shcmd)
        self._logger.info("[config.xml] rename unknown_proc_num -> %s", self.Proc_Num)

        # modify xxx.xml.bak
        os.chdir(dst_dir)
        os.chdir(r"./build_directory/data/bossapp/monitor/data")

        shcmd = "sed -i 's/unknown_rpm/" + self.Rpm_Package + "/g' unknown.xml.bak"
        os.system(shcmd)
        self._logger.info("[unknown.xml.bak] rename unknown_rpm -> %s", self.Rpm_Package)

        shcmd = "sed -i 's/unknown_proc/" + self.Executable_file + "/g' unknown.xml.bak" 
        os.system(shcmd)
        self._logger.info("[unknown.xml.bak] rename unknown_proc -> %s", self.Executable_file)

        shcmd = "sed -i 's/unknown_num/" + self.Proc_Num + "/g' unknown.xml.bak"
        os.system(shcmd)
        self._logger.info("[unknown.xml.bak] rename unknown_num -> %s", self.Proc_Num)

        # modify spec
        os.chdir(dst_dir)
        spec_file =  "unknown.spec"
        shcmd = "sed -i 's/unknown_rpm_package/" + self.Rpm_Package + "/g' " + spec_file 
        os.system(shcmd)           
        self._logger.info("[%s] rename unknown_rpm_package ->%s", spec_file, self.Rpm_Package)

        shcmd = "sed -i 's/unknwon_monitor.xml/" + self.Monitor_File + "/g' remote_cntrol_conf"  
        os.system(shcmd)           
        self._logger.info("[remote_cntrol_conf] rename unknwon_monitor.xml ->%s", self.Monitor_File)

        # modify file-----------end-------------------------------------------------------------------------------------------------------


        rmp_package_path = r"./build_directory/data/bossapp/" + self.Rpm_Package

        # rename file-----------begin-------------------------------------------------------------------------------------------------------
        #rename Executable_file
        os.chdir(dst_dir)
        bin_path = r"./build_directory/data/bossapp/" + self.Rpm_Package + os.sep + "bin"    
        os.chdir(bin_path)
        os.rename(r"unknown", self.Executable_file)
        self._logger.info("[%s] rename unknown executable_file ->%s", bin_path, self.Executable_file)

        #rename xxx.xml.bak
        os.chdir(dst_dir)
        os.chdir("./build_directory/data/bossapp/monitor/data")
        os.rename("unknown.xml.bak", self.Monitor_File + ".bak")
        self._logger.info("[./build_directory/data/bossapp/monitor/data] unknown.xml.bak ->%s", self.Monitor_File + ".bak")
        
        os.chdir(dst_dir)
        os.rename(r"unknown.spec", self.Rpm_Package + ".spec")
        self._logger.info("[%s] rename unknown.spec ->%s", dst_dir, self.Rpm_Package + ".spec")
        # rename file-----------end-------------------------------------------------------------------------------------------------------

        # create symbol link
        os.chdir(dst_dir)
        os.chdir(rmp_package_path)
        shcmd = "rm -rf logs"
        os.system(shcmd)
        shcmd = "ln -s /data/bossapp/logs/" +  self.LogDir_Name + " logs"
        os.system(shcmd)


      
 
        shcmd = r"tree " + dst_dir
        os.system(shcmd)

if __name__ == '__main__':
    log_file = os.path.relpath(sys.argv[0])[0:-3] + ".log"
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        filename=log_file,
                        filemode='w')
    _src_dir = r"./daemon_template"
    if not os.path.isdir(_src_dir):
        print(" Error %s is not a dir" % _src_dir)
        os._exit(0)

    _xmlconf = r"./jats_daemon_template.xml"
    if not os.path.exists(_xmlconf):
        print('Error: %s not exist' % _xmlconf)
        os._exit(0)

    obj = DaemonTemplate(_src_dir, _xmlconf)
    obj.create_jats_daemon_dir()