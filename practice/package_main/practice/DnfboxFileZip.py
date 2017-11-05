# coding:utf-8

from ..pythoncookbook.chapter2_file.fileprocess import *

def ZipDNFUpdateFiles():
    newModelCfgPath = r"F:\DNF盒子\DNF发版\box\DNF数据目录\DNF数据库\时装\ModelCfg\分类结果"
    newModelCfgZipPath = r"F:\DNF盒子\DNF发版\box\DNF数据目录\DNF数据库\时装\ModelCfg\分类结果"
    zip_dir(newModelCfgPath, newModelCfgZipPath)
