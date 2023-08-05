#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/26 7:52 下午
# @Author  : lijiarui
# @Email   : lijiarui15@jd.com
# @Site    : 
# @File    : logger.py
# @Software: PyCharm
"""
cache logger for use client
optional output to log file or terminal
"""
import logging


def getLogger(name=None):
    logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.propagate = False

    return logger


logger = getLogger('nacos_client')


def init(level):
    logging.addLevelName(logging.CRITICAL + 10, 'OFF')
    logger.setLevel(logging.getLevelName(level))