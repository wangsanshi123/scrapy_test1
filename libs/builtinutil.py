#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
内置方法的一些封装改良
'''


import warnings
from collections import defaultdict
import os.path

warnings.filterwarnings('ignore')
__author__ = 'yangsheng'

def join(arrlike, spliter):
    '''
    将集合组合为字符串
    :param arrlike: list/set/tuple
    :param spliter:
    :return:
    '''
    return str(spliter).join([str(x) for x in arrlike])

def add_each(a, b):
    return [sum(x) for x in zip(a, b)]

def div(fenzi, fenmu):
    return float(fenzi)/(float(fenmu) or 1)

def split(sen, splitter=' ', del_null=True):
    sen = str(sen)
    if del_null:
        return [x.strip() for x in sen.split(splitter) if x.strip()]
    else:
        return [x.strip() for x in sen.split(splitter)]

def contain(x, y):
    return y in x

def same(set1, set2):
    '''
    两个组合内的内容化为 set 后是否完全相同
    :param set1:
    :param set2:
    :return:
    '''
    return len(set1) == len(set2) and len([x for x in set1 if not x in set2]) == 0

def sum_dictin(dict_1_2):
    '''
    两层字典，使用内层键作为求和键，返回字典；
    :param dict_1_2:
    :return:
    '''
    if not isinstance(dict_1_2, dict):
        raise Exception('builtin.sum_dictin', 'param should in dict_dict_num type')
    dict_out = defaultdict(float)
    for key1, dict2 in dict_1_2.items():
        if not isinstance(dict2, dict):
            raise Exception('builtin.sum_dictin', 'param should in dict_dict_num type')
        for key, value in dict2.items():
            dict_out[key] += value
    return dict_out

def exists(filepath):
    '''
    文件是否存在且不为空，只能用于检测文件，不能用于文件夹
    :param filepath:
    :return:
    '''
    return os.path.exists(filepath) and os.path.getsize(filepath) > 0


if __name__ == '__main__':
    print(add_each([0, 1, 2], [3, 3, 3]))