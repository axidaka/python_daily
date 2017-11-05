#coding:utf-8

import os
import shutil
#

lstImgPath = list()

def collect_qq_imgcache(rootPath):
    '删除QQ聊天缓存图片'

    if os.path.isdir(rootPath):
        listItems = os.listdir(rootPath)

        for item in listItems:
            fullpath = os.path.join(rootPath, item)

            if os.path.isdir(fullpath):
                collect_qq_imgcache(fullpath)
            else:
                (filename, filetype) = os.path.splitext(item)
                if (len(filetype) != 0) and (filetype == '.gif' or filetype == '.jpg'):
                    lstImgPath.append(fullpath)
                    print item, len(lstImgPath)
        
def delect_files(files):
    
    lstImg = os.listdir(r"G:\\test\\qqimgcache")
    nCount = len(lstImg)
    for item in files:
        (filename, filetype) = os.path.splitext(item)
        dstpath = r"G:\\test\\qqimgcache\\%d%s"%(nCount, filetype)
        nCount += 1
        shutil.move(item, dstpath)





def delete_repeatpng(rootPath, dstPath):
    '删除时装图标重复图标 1.扫描根目录下所有职业ID目录, 2 扫描职业下除了weapon目录'
    
    print '正在扫描目录:', rootPath
    
    if os.path.isdir(rootPath):
        
        delete_count = 1
        listIDs = os.listdir(rootPath)
        #根目录下第一层目录是职业ID目录
        for item_ID in listIDs:
            if (item_ID != 'unknown.jpg'):
                print item_ID

                profession_path = os.path.join(rootPath, item_ID)
                dst_firstlevel_path = os.path.join(dstPath, item_ID)
                print profession_path, dst_firstlevel_path

                if os.path.isdir(profession_path):
                    listAvatars = os.listdir(profession_path)
                    #根目录下第二层目录是时装部位
                    for item_Avatar in listAvatars:
                        if (item_Avatar != 'weapon'):
                            
                            avatar_path = os.path.join(profession_path, item_Avatar)
                            dst_secondlevel_path = os.path.join(dst_firstlevel_path, item_Avatar)
                            if (not os.path.exists(dst_secondlevel_path)):
                                os.makedirs(dst_secondlevel_path)

                            print avatar_path, dst_secondlevel_path

                            list_Pngs = os.listdir(avatar_path)
                            for item_png in list_Pngs:
                                if (-1 == item_png.find('_')):
                                    print item_png, delete_count
                                    delete_count += 1
                                    png_path = os.path.join(avatar_path, item_png)
                                    dst_png_path = os.path.join(dst_secondlevel_path, item_png)
                                    if (not os.path.exists(dst_png_path)):
                                        shutil.move(png_path, dst_png_path)

                        else:
                           print '不处理武器'.decode('utf-8').encode('gbk'), item_Avatar
    
    else:
        print '请输入正确目录路径'       



if __name__ == "__main__":
    #rootPath = r"E:\工作区\DNFBox\DNF盒子代码\早期DNF\DNF版本管理\DnfModel\Icon\ModelItemIcon"
    #dstPath = r"C:\backup"
    #delete_repeatpng(rootPath.decode('utf-8').encode('gbk'), dstPath.decode('utf-8').encode('gbk'))
    rootpath = r"D:\用户目录\我的文档\Tencent Files"
    collect_qq_imgcache(rootpath.decode('utf-8').encode('gbk'));
    delect_files(lstImgPath) 
   