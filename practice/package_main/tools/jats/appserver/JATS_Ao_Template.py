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


class AoTemplate(object):

    def __init__(self, _src_dir, _xmlconf):
        self._logger = logging.getLogger(__name__)
        self.src_dir = _src_dir
        self.load_xmlconf(_xmlconf)

    def load_xmlconf(self, xmlconf):

        self._logger.debug("load xmlconf: %s", xmlconf)
        DOMTree = xml.dom.minidom.parse(xmlconf)
        JATS_TWS_Template_conf = DOMTree.documentElement
        conf = JATS_TWS_Template_conf.getElementsByTagName("conf")
        for item in conf:
            self.Rpm_Package = item.getElementsByTagName("Rpm_Package")[0].childNodes[0].data
            self.Ao_So = item.getElementsByTagName("Ao_So")[0].childNodes[0].data
            self.Ao_Service_Name = item.getElementsByTagName("Ao_Service_Name")[0].childNodes[0].data
            self.Ao_Port = item.getElementsByTagName("Port")[0].childNodes[0].data
            self.Monitor_File = item.getElementsByTagName("Monitor_File")[0].childNodes[0].data

    def create_jats_tws_dir(self):
        dst_dir = os.getcwd() + os.sep + self.Rpm_Package + os.sep
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
        os.rename(r"unknown_logdir", self.Rpm_Package)
        self._logger.info("[./build_directory/data/bossapp/logs] rename unknown_logdir->%s", self.Rpm_Package)
        # rename dir-----------end-------------------------------------------------------------------------------------------------------

        rpm_path = dst_dir + r"./build_directory/data/bossapp/" + self.Rpm_Package + os.sep

        # modify file-----------begin-------------------------------------------------------------------------------------------------------
        # modify manage.sh
        os.chdir(rpm_path + "bin")
        shcmd = "sed -i 's/ao_unknown_service/" + self.Ao_Service_Name + "/g' manage.sh"
        os.system(shcmd)
        self._logger.info("[manage.sh] rename ao_unknown_service -> %s", self.Ao_Service_Name)

        #modify appchn_xxx.xml
        os.chdir(rpm_path + "conf")
        conf_file = "appchn_ao_unknown_service.xml"
        shcmd = "sed -i 's/unknown_logdir/" + self.Rpm_Package + "/g' " + conf_file
        os.system(shcmd)

        shcmd = "sed -i 's/unknown_port/" + self.Ao_Port + "/g' " + conf_file
        os.system(shcmd)

        #modify appsvc_xxx.xml
        conf_file = "appsvc_ao_unknown_service.xml"
        shcmd = "sed -i 's/unknown_logdir/" + self.Rpm_Package + "/g' " + conf_file
        os.system(shcmd)

        shcmd = "sed -i 's/unknown_port/" + self.Ao_Port + "/g' " + conf_file
        os.system(shcmd)

        shcmd = "sed -i 's/unknown.so/" + self.Ao_So + "/g' " + conf_file
        os.system(shcmd)
        
        #modify xxx.xml.bak
        os.chdir(dst_dir)
        os.chdir("./build_directory/data/bossapp/monitor/data")

        shcmd = "sed -i 's/unknown_rpm/" + self.Rpm_Package + "/g' unknown.xml.bak" 
        os.system(shcmd)

        shcmd = "sed -i 's/ao_unknown_service/" + self.Ao_Service_Name + "/g' unknown.xml.bak" 
        os.system(shcmd)


         # modify spec
        os.chdir(dst_dir)
        spec_file = "ao_service_unknown.spec"
        shcmd = "sed -i 's/unknown_rpm_package/" + self.Rpm_Package + "/g' " + spec_file 
        os.system(shcmd)           
        self._logger.info("[%s] rename unknown_rpm_package ->%s", spec_file, self.Rpm_Package)

        shcmd = "sed -i 's/unknwon_monitor.xml/" + self.Monitor_File + "/g' remote_cntrol_conf"  
        os.system(shcmd)           
        self._logger.info("[remote_cntrol_conf] rename unknwon_monitor.xml ->%s", self.Monitor_File)

        # modify file-----------end-------------------------------------------------------------------------------------------------------


        # rename file-----------begin-------------------------------------------------------------------------------------------------------
        #rename xml.bak file
        os.chdir(dst_dir)
        os.chdir("./build_directory/data/bossapp/monitor/data")
        os.rename("unknown.xml.bak", self.Monitor_File + ".bak")
        self._logger.info("[./build_directory/data/bossapp/monitor/data] unknown.xml.bak ->%s", self.Monitor_File + ".bak")

        #rename so file
        ao_so_path = rpm_path + "plugin"        
        os.chdir(ao_so_path)
        os.rename(r"unknown.so", self.Ao_So)
        self._logger.info("[%s] rename unknown.so ->%s", ao_so_path, self.Ao_So)

        bin_path = rpm_path + "bin"
        os.chdir(bin_path)

        shcmd = "ln -s /data/bossapp/appserver64/bin/appchn.2.0 appchn_" +  self.Ao_Service_Name
        os.system(shcmd)

        shcmd = "ln -s /data/bossapp/appserver64/bin/appsvc.2.0 appsvc_" +  self.Ao_Service_Name
        os.system(shcmd)
        
        conf_path = rpm_path + "conf"
        os.chdir(conf_path)
        os.rename(r"appchn_ao_unknown_service.xml", "appchn_" + self.Ao_Service_Name + ".xml")
        self._logger.info("[%s] rename appchn_ao_unknown_service.xml ->%s", conf_path, "appchn_" + self.Ao_Service_Name + ".xml")
        os.rename(r"appsvc_ao_unknown_service.xml", "appsvc_" + self.Ao_Service_Name + ".xml")
        self._logger.info("[%s] rename appsvc_ao_unknown_service.xml ->%s", conf_path, "appsvc_" + self.Ao_Service_Name + ".xml")

        os.chdir(dst_dir)
        os.rename(r"ao_service_unknown.spec", self.Rpm_Package + ".spec")
        self._logger.info("[%s] rename ao_service_unknown.spec ->%s", dst_dir, self.Rpm_Package + ".spec")
        # rename file-----------end-------------------------------------------------------------------------------------------------------

      
        # create symbol link
        os.chdir(rpm_path)
        shcmd = "rm -r log"
        os.system(shcmd)
        shcmd = "ln -s /data/bossapp/logs/" +  self.Rpm_Package + " log"
        os.system(shcmd)

        shcmd = r"tree " + dst_dir
        os.system(shcmd)

if __name__ == '__main__':
    log_file = os.path.relpath(sys.argv[0])[0:-3] + ".log"
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        filename=log_file,
                        filemode='w')
    _src_dir = r"./ao_template"
    if not os.path.isdir(_src_dir):
        print(" Error %s is not a dir" % _src_dir)
        os._exit(0)

    _xmlconf = r"./jats_ao_template.xml"
    if not os.path.exists(_xmlconf):
        print('Error: %s not exist' % _xmlconf)
        os._exit(0)

    obj = AoTemplate(_src_dir, _xmlconf)
    obj.create_jats_tws_dir()