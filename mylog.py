#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import getpass
import sys

'''
简单的日志模块,直接输出信息
'''


class MyLog(object):
    def __init__(self, logfile):
        self.user = getpass.getuser()
        self.logger = logging.getLogger(self.user)
        self.logger.setLevel(logging.DEBUG)

        if logfile:
            self.logFile = logfile
        else:
            self.logFile = sys.argv[0][0:-3] + ".log"
        self.formatter = logging.Formatter("%(asctime)-12s %(levelname)-8s %(name)-10s %(message)-12s\r\n")
        self.logHand = logging.FileHandler(self.logFile, encoding="utf8")
        self.logHand.setFormatter(self.formatter)
        self.logHand.setLevel(logging.INFO)  # 设置写入门槛

        self.logHandSt = logging.StreamHandler()
        self.logHandSt.setFormatter(self.formatter)
        self.logHandSt.setLevel(logging.WARNING)

        self.logger.addHandler(self.logHand)
        self.logger.addHandler(self.logHandSt)

    def set_level(self, l):
        self.logHand.setLevel(l)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


if __name__ == "__main__":
    log = MyLog("m.log")
    log.set_level(logging.ERROR)
    log.debug("I'm debug 中文")
    log.info("I'm info")
    log.warn("I'm warning")
    log.error("I'm error 中文")
    log.critical("I'm critical 中文")
