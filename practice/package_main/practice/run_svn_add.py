#coding:utf-8

import sys
import os

def run_svn_add(dir):
    # 目录先执行 svn add 命令, 文件可以略过
    os.chdir(dir)
    cmdline = '"C:\\Program Files\\TortoiseSVN\\bin\\svn.exe" add * --force'
    #print cmdline
    os.system(cmdline)
    for path, subdirs, files in os.walk(dir):
        for diritem in subdirs:
            fullpath = os.path.join(path, diritem)
            os.chdir(fullpath)
            print fullpath
            os.system(cmdline)


def main():
    print "argv", sys.argv
    if len(sys.argv) <= 1:
        print "argv error"

    else:
        dir = sys.argv[1]
        print dir
        if not os.path.isdir(dir):
            print '%s 不是有效目录' % (dir)
        else:
            #run_svn_add(dir.decode('utf-8').encode('gbk'))
            # 如果命令行环境编码是gbk,并且传中文路径字符串, 这时候字符编码应该是gbk, 不需要进行decode encode
            run_svn_add(dir)

    # dir = r'E:\boxgroup\DNFBox\DNF盒子代码\新版DnfBox\branches\common\Common\ygdata_report_hiido'
    # run_svn_add(dir.decode('utf-8').encode('gbk'))


if __name__ == "__main__":
    main()