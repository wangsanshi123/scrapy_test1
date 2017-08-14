#!/usr/bin/python
# -*- coding: utf-8 -*-
import warnings
from collections import OrderedDict

import math

warnings.filterwarnings('ignore')
__author__ = 'yangsheng'

DICT_PLATFORM = OrderedDict({
                     '8916':['Y31', 'Y51', 'Y35A'],
                     '8937':['Y55A', 'Y66'],
                     '8939':['V3MaxA', 'V3', 'X6A', 'X6PlusA', 'X5ProV', 'Y37'],
                     '6735':['Y33', 'Y35'],
                     '6750':['V3MA', 'Y67'],
                     '6752':['X5ProD', 'X6D', 'X6PlusD'],
                     '8953':['X9', 'X9i'],
                     '8976':['X9Plus','X6SA', 'X6SPlusA', 'X6SPlusD', 'X7', 'X7Plus', 'Xplay5A'],
                     '8996':['Xplay5S', 'Xplay6']})
DICT_MOD_PLAT = {}
for plat, mods in DICT_PLATFORM.items():
    for mod in mods:
        DICT_MOD_PLAT[mod] = plat





MODELS = ['X6A', 'X6D', 'X6PlusA', 'X6PlusD', "Y51", 'X5L', 'X5Max+', 'X5MaxL', 'X5MaxV', 'X5M', 'X5ProD',
 'X5ProD25', 'X5ProV',
 'X5SL', 'X5V', 'Xplay3S', 'Xshot', 'Y13iL', 'Y13L', 'Y22iL', 'Y22L', 'Y23L', 'Y27',
 'Y28L', 'Y29L', "Y31", 'Y33', 'Y37', 'Y35', 'Y35A', 'Xplay5A', 'X6SA', 'X6SPlusA', 'X6SPlusD', 'V3MaxA', 'V3',
 'V3MA',
 'Xplay5S', 'X7', 'X7Plus', 'Y55A', 'X9', 'Xplay6', 'Y67', 'X9Plus', 'X9i', 'Y66']

def ver_to_num(version):
    '''
    将软件版本号转化为数值，用于比较版本号大小
    版本号越大，获得返回值越大
    非法版本号将返回值 0
    '''
    arr = version.split(".")
    curbit = 0
    ver_num = 0
    for num in arr[-1::-1]:
        #08.06.03 这种版本号视作非法
        if num and len(num) > 1 and num[0] == '0':
            return 0
        try:
            ver_num += int(num) * math.pow(100, curbit)
            curbit += 1
        except Exception:
            return 0
    return ver_num


def get_series(modelname):
    modelname = modelname.replace(' ', '').lower()
    if modelname.startswith('vivoxplay'):
        return 'Xplay系列'
    elif modelname.startswith('vivox'):
        return 'X系列'
    elif modelname.startswith('vivoy'):
        return 'Y系列'
    elif modelname.startswith('vivov'):
        return 'V系列'
    else:
        return '其他'

