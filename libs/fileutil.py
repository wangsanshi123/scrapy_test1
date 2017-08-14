#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import os
import warnings
import sys
import glob

import shutil

warnings.filterwarnings('ignore')
__author__ = 'yangsheng'

def copyfolder(folder_src, folder_dest):
    '''
    拷贝文件夹的所有文件，有待改进
    :param folder_src:
    :param folder_dest:
    :return:
    '''
    for filepath in glob.glob('%s\*'%folder_src):
        basename = os.path.basename(filepath)
        destpath = '%s\\%s'%(folder_dest, basename)
        shutil.copy(filepath, destpath)


def get_filelist_recursive(folder, suffix='', seg=''):
    '''
    递归查询目录
    :param folder: 根目录
    :param suffix: 后缀，'' 或 None 表示不限制后缀
    :param seg: 文件名中包含的片段
    :return:
    '''
    listpath = list()
    for folderpath, dirlist, filelist in os.walk(folder):
        for file in filelist:
            if not suffix or file.endswith(suffix if '.' in suffix else '.'+suffix):
                if not seg or seg in os.path.basename(file):
                    # print('%s%s%s'%(folderpath, os.path.sep, file))
                    listpath.append('%s%s%s'%(folderpath, os.path.sep, file))
        for fd in dirlist:
            listpath += get_filelist_recursive(fd, suffix, seg)

    return listpath

def get_filelist_recursive_iter(folder, suffix='', seg=''):
    '''
    递归查询目录，yield模式
    :param folder: 根目录
    :param suffix: 后缀，'' 或 None 表示不限制后缀
    :param seg: 文件名中包含的片段
    :return:
    '''
    for folderpath, dirlist, filelist in os.walk(folder):
        for file in filelist:
            if not suffix or file.endswith(suffix):
                if not seg or seg in os.path.basename(file):
                    yield '%s%s%s'%(folderpath, os.path.sep, file)


def get_folderlist_recursive(folder, str_tofind):
    listpath = list()
    for folderpath, dirlist, filelist in os.walk(folder):
        for file in dirlist + filelist:
            if str_tofind in file:
                listpath.append('%s%s%s'%(folderpath, os.path.sep, file))
    return listpath

def search(folder, seg, search_onlyfilename=True, suffix=None):
    '''
    在指定目录中递归查询指定字符串
    :param folder: 待查询目录
    :param seg: 待查询字符串
    :param search_onlyfilename: 是否只查询文件名
    :param suffix: 文件名后缀
    :return: 格式：[[文件路径, 字符串出现的行号, 字符串出现的行],……]
    '''
    filelist = get_filelist_recursive(folder, suffix)
    list_out = list()
    print('查找文件数：' + str(len(filelist)))
    for filepath in filelist:
        filepath_afterfolder = filepath[len(folder):]
        if seg in filepath_afterfolder:
            list_out.append([filepath, 0, ''])
        if search_onlyfilename:
            continue
        lineindex = 0
        try:
            with codecs.open(filepath, 'r', 'utf-8') as f:
                for line in f:
                    lineindex += 1
                    if seg in line:
                        list_out.append([filepath, lineindex, line.strip()])
        except:
            print('error: ' + filepath)
    return list_out

def test():
    # get_folderlist_recursive(r'E:\newweekreport\weekreport', 'xlsm')
    # listfile = get_filelist_recursive_iter(r'F:\工作\高耗电统计\X7_new\X7\vivoX7', suffix='txt', seg='1101_1_2016')
    # listfile = get_filelist_recursive_iter(r'E:', suffix='py', seg='网络社交类用户')
    listfile = search(r'F:\\', suffix='py', seg='模型',search_onlyfilename=False)
    # print(len(listfile))
    for file in listfile:
        print(file)


if __name__ == '__main__':
    test()
    # args = sys.argv[1:]
    # folder = None
    # search_onlyfilename = False
    # seg = None
    # suffix = None
    # if len(args) == 4:
    #     folder, seg, search_onlyfilename, suffix = args[0], args[1], str(args[2]).lower() == 'true', args[3]
    # else:
    #     raise Exception('传入4个参数：参数1为搜索文件夹名，参数2为搜索字符串，参数3为是否只搜索文件名(True/False，默认False)，参数4为文件名后缀')
    # listfiles = search(folder, seg, search_onlyfilename, suffix)
    # for filepath, index, line in listfiles:
    #     print(filepath, index, line)