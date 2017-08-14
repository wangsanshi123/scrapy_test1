#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import warnings

import timeutil

warnings.filterwarnings('ignore')
__author__ = 'yangsheng'

logger_main = None

class VivoLogger(object):

    def __init__(self, folder, name, console=True, shiftday=True):
        self.folder = folder if folder.endswith('/') else folder + '/'
        self.console = console
        self.shiftday = shiftday
        self.logger = logging.Logger(name)
        self.formatter = logging.Formatter('%(name)-8s:%(levelname)-6s %(asctime)s %(message)s')
        self.file_hand = None
        self._init_filehand()
        if console:
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            console.setFormatter(self.formatter)
            self.logger.addHandler(console)

    def _init_filehand(self):
        if self.file_hand:
            self.logger.removeHandler(self.file_hand)
        if self.shiftday:
            self.basename = '%s_%s.txt' % (self.logger.name, timeutil.date_today())
        else:
            self.basename = '%s.txt' % self.logger.name
        self.filepath = '%s%s' % (self.folder, self.basename)
        self.file_hand = logging.FileHandler(self.filepath, mode='a', encoding='utf-8')
        self.file_hand.setLevel(logging.DEBUG)
        self.file_hand.setFormatter(self.formatter)
        self.logger.addHandler(self.file_hand)

    def log(self, level, msg):
        if self.shiftday and not self.basename == '%s_%s.txt' % (self.logger.name, timeutil.date_today()):
            self._init_filehand()
        self.logger.log(level, msg)

    def info(self, msg):
        self.log(logging.INFO, msg)

    def error(self, msg):
        self.log(logging.ERROR, msg)

    def debug(self, msg):
        self.log(logging.DEBUG, msg)

    def warn(self, msg):
        self.log(logging.WARN, msg)

def new_logger(folder, name, console=True, shiftday=True):
    return VivoLogger(folder, name, console=console, shiftday=shiftday)

