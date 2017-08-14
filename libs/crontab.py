#!/usr/bin/python
# -*- coding: utf-8 -*-
import warnings
import baseutil
warnings.filterwarnings('ignore')
__author__ = 'yangsheng'

class Crontab(object):

    def __init__(self):
        pass

    def run_daily(self, datea):
        pass

    def run_weekly(self, datea):
        pass

    def run_monthly(self, datea):
        pass

    def init_data(self):
        pass

    def get_logfile(self):
        raise Exception('Crontab subclass should overwrite function get_logfile')

    def writelog(self, logline):
        baseutil.writelog(logline, self.get_logfile())