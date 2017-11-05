#coding:utf-8

import win32process
import time
import os

def run_dnfbox():

    while (True):

        strExepath = r"E:\\boxgroup\\DNFBox\\DNF盒子代码\\新版DnfBox\\trunk\\product\\bin\\win32\\Debug\\DnfBoxClient.exe"
        
        pTuple =  win32process.CreateProcess(strExepath.decode('utf-8').encode('gbk'), '', None , None , 0 ,win32process. CREATE_NO_WINDOW , None , None ,win32process.STARTUPINFO())

        if (0 == len(pTuple)):
            print "Create Process Fail"

        print "Create Process Success"

        time.sleep(15)

        pList = win32process.EnumProcesses()
        if (pTuple[2] in pList):
            print "Terminate Process"
            exiCode = 0;
            win32process.TerminateProcess(pTuple[0], exiCode)

        time.sleep(2)

        lstDir = os.listdir(u"E:\\boxgroup\\崩溃调试\\Dump")
        if (0 != len(lstDir)):
            for item in lstDir:
                if (-1 != item.find("dmp")):
                    return;


if __name__ == "__main__":
    run_dnfbox();