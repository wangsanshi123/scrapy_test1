#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import types
import warnings
import os
from multiprocessing.pool import Pool

import time

warnings.filterwarnings('ignore')
__author__ = 'yangsheng'

def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

# copy_reg.pickle(types.MethodType, _pickle_method)

class MultiProcessor(object):

    def __init__(self, channel_folder, jobs=-1):
        self._channel_folder = channel_folder
        self._jobs = jobs
        self._pool = Pool(processes=jobs)

    def map(self):
        self._pool.map()


class OOO(object):

    def __init__(self, a):
        self.a = a
    def ooofunc(self, x, y):
        time.sleep(3)
        print(os.getpid(), x, y, self.a+x + y)
        return self.a + x

def funca(x):
    print(os.getpid(), x)
    return x

def funcb(x):
    print(os.getpid(), x + 1)
    # time.sleep(3)
    return x+ 1

def testresult():
    poola = Pool(processes=3)
    results = poola.map(funca, [[1,2],(2,3), (3,4)])
    print(results)

def testresult2():
    print(os.getpid())
    poola = Pool(processes=3)
    results = list()
    timestart = time.time()
    oooa = OOO(3)
    for i in range(5):
        result = poola.apply_async(oooa.ooofunc, [1], callback=funcb)
        results.append(result)
    for result in results:
        result.wait()
    # time.sleep(100)
    # print (result.get())
    timeend = time.time()
    print(timeend-timestart)

class AAAAA(object):

    def __init__(self, pool, a):
        self.a = a
        self._poola = pool

    def funca(self, x):
        print(os.getpid(), x, x + 4)
        time.sleep(3)
        return x

    def funcb(self, x):
        print(os.getpid(), x + 1)
        # time.sleep(3)
        return x + 1

    @staticmethod
    def ooofunc(x):
        x,y = x
        time.sleep(3)
        print(os.getpid(), x, y, x + y)
        return x

    def testresult(self):
        poola = Pool(processes=3)
        results = poola.map(funca, [[1, 2], (2, 3), (3, 4)])
        print(results)

    def testresult2(self):
        print(os.getpid())
        results = list()
        # oooa = OOO(3)
        timestart = time.time()
        poola = Pool(processes=2)
        for i in range(5):
            result = self._poola.map(AAAAA.ooofunc, [(1, 2), (2, 3), (4,4)])
            results.append(result)
        for result in results:
            result.wait()
        # time.sleep(100)
        # print (result.get())
        timeend = time.time()
        print(timeend - timestart)


if __name__ == '__main__':
    # testresult2()
    AAAAA(Pool(3), 3).testresult2()