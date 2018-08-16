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


class TwsTemplate(object):

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
            self.Domain = item.getElementsByTagName("Domain")[0].childNodes[0].data
            self.Url_Pattern = item.getElementsByTagName("Url_Pattern")[0].childNodes[0].data
            self.Rpm_Package = item.getElementsByTagName("Rpm_Package")[0].childNodes[0].data
            self.Tws_Service_Name = item.getElementsByTagName("Tws_Service_Name")[0].childNodes[0].data
            self.Tws_So = item.getElementsByTagName("Tws_So")[0].childNodes[0].data
            self.LogDir_Name = item.getElementsByTagName("LogDir_Name")[0].childNodes[0].data
            self.Connector_Queue_Key = item.getElementsByTagName('Connector_Queue_Key')[0].childNodes[0].data
            self.Timeout_Report_Key = item.getElementsByTagName('Timeout_Report_Key')[0].childNodes[0].data

    def create_jats_tws_dir(self):
        dst_dir = os.getcwd() + os.sep + self.Rpm_Package
        rmcmd = "rm -rf %s" % (dst_dir)
        os.system(rmcmd)

        shcmd = r"cp -r %s %s" % (self.src_dir, dst_dir)
        os.system(shcmd)

        # rename dir-----------begin-------------------------------------------------------------------------------------------------------
        #rename rpm_package
        os.chdir(dst_dir)
        os.chdir(r"./build_directory/usr/local/webapps")
        os.rename(r"unknown", self.Rpm_Package)
        self._logger.info("[./build_directory/usr/local/webapps] rename unknown->%s", self.Rpm_Package)

        #rename logdir 
        os.chdir(dst_dir)        
        os.chdir(r"./build_directory/data/webapps_log")
        os.rename(r"unknown_logdir", self.LogDir_Name)
        self._logger.info("[./build_directory/data/webapps_log] rename unknown->%s", self.LogDir_Name)
        # rename dir-----------end-------------------------------------------------------------------------------------------------------

        # rename file-----------begin-------------------------------------------------------------------------------------------------------
        #rename so file
        os.chdir(dst_dir)
        tws_so_path = r"./build_directory/usr/local/webapps/" + self.Rpm_Package + os.sep + "service"        
        os.chdir(tws_so_path)
        os.rename(r"unknown.so", self.Tws_So)
        self._logger.info("[%s] rename unknown.so ->%s", tws_so_path, self.Tws_So)

        os.chdir(dst_dir)
        os.chdir(r"./build_directory/usr/local/webserver/conf")
        os.rename(r"TwsVhost_unknown.wq.jd.com.xml", "TwsVhost_" + self.Tws_Service_Name + ".wq.jd.com.xml")
        self._logger.info("[./build_directory/usr/local/webserver/conf] rename TwsVhost_unknown.wq.jd.com.xml ->%s", "TwsVhost_" + self.Tws_Service_Name + ".wq.jd.com.xml")
        
        os.chdir(dst_dir)
        os.rename(r"web_service_unknown.spec", self.Rpm_Package + ".spec")
        self._logger.info("[%s] rename web_service_unknown.spec ->%s", dst_dir, self.Rpm_Package + ".spec")
        # rename file-----------end-------------------------------------------------------------------------------------------------------

        # modify file-----------begin-------------------------------------------------------------------------------------------------------
        # modify service.xml
        os.chdir(dst_dir)
        rmp_package_path = r"./build_directory/usr/local/webapps/" + self.Rpm_Package
        os.chdir(rmp_package_path + os.sep + "bin")
        shcmd = "sed -i 's/unknown_tws/" + self.Tws_Service_Name + "/g' service_manager.sh"
        os.system(shcmd)
        self._logger.info("[service_manager.sh] rename unknown_tws -> %s", self.Tws_Service_Name)

        os.chdir("../conf")
        shcmd = "sed -i 's/unknown.com/" + self.Domain + "/g' service.xml"
        os.system(shcmd)
        self._logger.info("[service.xml] rename unknown.com -> %s", self.Domain)

        shcmd = "sed -i 's/unknown_rpm_package/" + self.Rpm_Package + "/g' service.xml"
        os.system(shcmd)
        self._logger.info("[service.xml] rename unknown_rpm_package ->%s", self.Rpm_Package)

        shcmd = "sed -i 's/unknown_url_pattern/" + self.Url_Pattern + "/g' service.xml"
        os.system(shcmd)
        self._logger.info("[service.xml] rename unknown_url_pattern ->%s", self.Url_Pattern)
        
        shcmd = "sed -i 's/unknown.so/" + self.Tws_So + "/g' service.xml"
        os.system(shcmd)
        self._logger.info("[service.xml] rename unknown.so ->%s", self.Tws_So)

        # modify webcontainer.xml
        shcmd = "sed -i 's/unknown_queue_key/" + self.Connector_Queue_Key + "/g' webcontainer.xml"
        os.system(shcmd)
        self._logger.info("[webcontainer.xml] rename unknown_queue_key ->%s", self.Connector_Queue_Key)

        shcmd = "sed -i 's/unknown_report_key/" + self.Timeout_Report_Key + "/g' webcontainer.xml"
        os.system(shcmd)
        self._logger.info("[webcontainer.xml] rename unknown_report_key -> %s", self.Timeout_Report_Key)
        
        # modify webserver xml
        os.chdir(dst_dir)
        os.chdir(r"./build_directory/usr/local/webserver/conf")
        webserver_conf_xml = "TwsVhost_" + self.Tws_Service_Name + ".wq.jd.com.xml"
        shcmd = "sed -i 's/unknown.com/" + self.Domain + "/g' " + webserver_conf_xml
        os.system(shcmd)
        self._logger.info("[%s] rename unknown.com -> %s", webserver_conf_xml, self.Domain)

        shcmd = "sed -i 's/unknown_queue_key/" + self.Connector_Queue_Key + "/g' " + webserver_conf_xml
        os.system(shcmd)
        self._logger.info("[%s] rename unknown_queue_key -> %s", webserver_conf_xml, self.Connector_Queue_Key)
        
        # modify spec
        os.chdir(dst_dir)
        spec_file = self.Rpm_Package + ".spec"
        shcmd = "sed -i 's/unknown_rpm_package/" + self.Rpm_Package + "/g' " + spec_file 
        os.system(shcmd)           
        self._logger.info("[%s] rename unknown_rpm_package ->%s", spec_file, self.Rpm_Package)

        shcmd = "sed -i 's/unknown_tws/" + self.Tws_Service_Name + "/g' " + spec_file
        os.system(shcmd)            
        self._logger.info("[%s] rename unknown_tws ->%s", spec_file, self.Tws_Service_Name)

        shcmd = "sed -i 's/unknown_logdir/" + self.LogDir_Name + "/g' " + spec_file
        os.system(shcmd)            
        self._logger.info("[%s] rename unknown_logdir ->%s", spec_file, self.LogDir_Name)

        shcmd = "sed -i 's/unknown.com/" + self.Domain + "/g' " + spec_file
        os.system(shcmd)            
        self._logger.info("[%s] rename unknown.com ->%s", spec_file, self.Domain)
        # modify file-----------end-------------------------------------------------------------------------------------------------------

        # create symbol link
        os.chdir(dst_dir)
        os.chdir(rmp_package_path)
        shcmd = "rm -r log"
        os.system(shcmd)
        shcmd = "ln -s /data/webapps_log/" +  self.LogDir_Name + " log"
        os.system(shcmd)

        shcmd = r"tree " + dst_dir
        os.system(shcmd)

if __name__ == '__main__':
    log_file = os.path.relpath(sys.argv[0])[0:-3] + ".log"
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        filename=log_file,
                        filemode='w')
    _src_dir = r"./web_service_template"
    if not os.path.isdir(_src_dir):
        print(" Error %s is not a dir" % _src_dir)
        os._exit(0)

    _xmlconf = r"./jats_tws_template.xml"
    if not os.path.exists(_xmlconf):
        print('Error: %s not exist' % _xmlconf)
        os._exit(0)

    obj = TwsTemplate(_src_dir, _xmlconf)
    obj.create_jats_tws_dir()