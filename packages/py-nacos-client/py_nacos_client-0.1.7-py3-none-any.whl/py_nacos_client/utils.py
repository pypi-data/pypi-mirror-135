#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/1/3 7:42 下午
# @Author  : lijiarui
# @Email   : lijiarui15@jd.com
# @Site    : 
# @File    : utils.py
# @Software: PyCharm

import os
import sys
import configparser
import socket
from py_nacos_client.logger import logger
# 当前文件路径
pro_dir = os.path.split(os.path.realpath(__file__))[0]
# 在当前文件路径下查找.ini文件

configPath = os.path.join(pro_dir, "./nacos_config.ini")
if configPath not in sys.path:
    sys.path.append(configPath)

conf = configparser.ConfigParser()
conf.read(configPath)

class NacosCenter(object):
    """
    Nacos connect info
    """
    def __init__(self, address, namespace, **kwargs):
        self.address = address
        self.namespace = namespace
        if kwargs:
            for k, v in kwargs:
                setattr(self, k, v)



def back_nacos_server():
    try:
        default_conf = conf.sections()[0]
    except IndexError:
        return "INI content not exist"
    server_addr = conf.get(default_conf, "SERVER_ADDRESSES")
    namespace = conf.get(default_conf, "NAMESPACE")
    na_obj = NacosCenter(address=server_addr,namespace=namespace)
    return na_obj

na_obj = back_nacos_server()



_local_ip = None


def get_host_ip():
    """
    get current ip addr
    :return:
    """
    global _local_ip
    s = None
    try:
        if not _local_ip:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            _local_ip = s.getsockname()[0]
        return _local_ip
    except:
        logger.warn("ERROR when get local host ip by socket connect", exc_info=True)
    finally:
        if s:
            s.close()


def synchronized_with_attr(attr_name):
    def decorator(func):
        def synced_func(*args, **kws):
            self = args[0]
            lock = getattr(self, attr_name)
            with lock:
                return func(*args, **kws)

        return synced_func

    return decorator