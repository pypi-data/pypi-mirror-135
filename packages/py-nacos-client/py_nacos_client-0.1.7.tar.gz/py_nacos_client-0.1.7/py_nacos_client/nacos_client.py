#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/26 11:25 下午
# @Author  : lijiarui
# @Email   : lijiarui15@jd.com
# @Site    : 
# @File    : nacos_client.py
# @Software: PyCharm

import atexit
import json
import re
import time
import random
import inspect
from copy import copy
from typing import Callable
from threading import Timer, RLock, Thread, Lock

import nacos
from py_nacos_client.logger import logger as _logger
from py_nacos_client.clienterror import  NoProvider
from py_nacos_client.utils import na_obj, synchronized_with_attr


"""
Status of instances
"""
INSTANCE_STATUS_UP: str = "UP"
INSTANCE_STATUS_DOWN: str = "DOWN"
INSTANCE_STATUS_STARTING: str = "STARTING"
INSTANCE_STATUS_OUT_OF_SERVICE: str = "OUT_OF_SERVICE"
INSTANCE_STATUS_UNKNOWN: str = "UNKNOWN"

"""
Action type of instances
"""
ACTION_TYPE_ADDED: str = "ADDED"
ACTION_TYPE_MODIFIED: str = "MODIFIED"
ACTION_TYPE_DELETED: str = "DELETED"

"""
The timeout seconds that all http request to the eureka server
"""
_DEFAULT_TIME_OUT = 5

"""
Default configurations
"""
_DEFAULT_ENCODING = "utf-8"


class HostsWrapper:

    def __init__(self, ip = "", port = "", weight = 0, healthy = False, **kwargs):
        """
        {
		"valid": true,
		"marked": false,
		"instanceId": "10.10.10.10-8888-DEFAULT-nacos.test.1",
		"port": 8888,
		"ip": "10.10.10.10",
		"weight": 1.0,
		"metadata": {}
	    }
        :param kwargs:
        """
        self.ip = ip
        self.port = port
        self.weight = weight
        self.healthy = healthy
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)

    def ip_str(self):
        return str(self.ip) + ":" + str(self.port)

    @property
    def is_valid(self):
        if self.healthy == "true" or self.healthy is True:
            return True
        else:
            return False

    def __eq__(self, other):
        return self.ip_str() == other.ip_str()



class ListenerBase:
    """
    subscribe callback deal
    modify client_ins content
    """
    def __init__(self, name, client_ins):
        self.listener_name = "default"
        self.client_ins = client_ins
        self.name = name


    def launch(self, *args):
        """
        订阅服务回调，修改目标服务注册信息
        :param args:
        :return:
        """
        local_sub_instance = args[1].instance
        status = args[0]
        new_host_obj = HostsWrapper(ip=local_sub_instance.pop('ip'), port=local_sub_instance.pop('port'),
                                    weight=local_sub_instance.pop('weight'), valid=local_sub_instance.pop('healthy'),
                                    **local_sub_instance
                                    )
        getattr(self, status.lower() + "_serverinfo")(new_host_obj)


    def added_serverinfo(self, new_host_obj):
        if new_host_obj.is_valid:
            self.client_ins.load_balance_dict[self.name]['ip_list'].append(new_host_obj)


    def modified_serverinfo(self, new_host_obj):
        if not new_host_obj.is_valid:
            self.deleted_serverinfo(new_host_obj)
        else:
            self.added_serverinfo(new_host_obj)

    def deleted_serverinfo(self, new_host_obj):
        ip_list = self.client_ins.load_balance_dict[self.name]['ip_list']
        if ip_list:
            for index, ip in enumerate(ip_list):
                if new_host_obj == ip:
                    ip_list.pop(index)
                    break



class JdPyNacosClient(nacos.NacosClient):
    """
    封装nacos客户端，减少参数的使用
    """

    _instance_lock = Lock()
    Register_already = set()

    def __new__(cls, *args, **kwargs):
        if not hasattr(JdPyNacosClient, "_instance"):
            with JdPyNacosClient._instance_lock:
                if not hasattr(JdPyNacosClient, "_instance"):
                    JdPyNacosClient._instance = object.__new__(cls)
        return JdPyNacosClient._instance

    def __init__(self, server_addresses, server_center=None):
        """
        :param server_addresses: nacos服务端单机
        :param server_list: nacos服务端集群
        """
        namespace = None
        if server_center:
            server_addresses = server_center.address
            namespace = server_center.namespace
        super().__init__(server_addresses, namespace=namespace,  endpoint=None,ak=None, sk=None, username=None, password=None)
        self.__heartbeat_interval = 3
        self.__heartbeat_timer = Timer(self.__heartbeat_interval, self.__auto_send_beat)
        self.__heartbeat_timer.daemon = True
        self.register_dict = {}
        self.instance_dict = {}
        self.load_balance_dict = {}
        self.deregister_lock = RLock()
        _logger.info("[client-init] endpoint:%s, tenant:%s" % (self.current_server, self.namespace))

    def __register(self, instance) -> None:
        try:
            regs = self.add_naming_instance(instance.service_name, ip=instance.ip,
                                                   port=instance.port, group_name=instance.group_name)
            if regs:
                self.Register_already.add(instance)
                _logger.info("服务注册成功。端口号:%s" % instance.port)
        except BaseException as e:
            _logger.error("服务注册失败。端口号:%s" % instance.port, exc_info=True)


    def __deregister(self, instance = None) -> None:
        """
        批量注销
        :param instance:
        :return:
        """
        map(self.do_deregister, self.Register_already) if len(self.Register_already) > 1 else self.do_deregister(list(self.Register_already)[0])

    @synchronized_with_attr("deregister_lock")
    def do_deregister(self, instance):
        try:
            regs = self.remove_naming_instance(instance.service_name, ip=instance.ip,
                                                       port=instance.port, group_name=instance.group_name)
            if regs:
                _logger.info("服务注销成功。")
        except:
            _logger.exception("服务注销失败", exc_info=True)

    @staticmethod
    def __is_ip(ip_str):
        return re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip_str)


    def __heart_beat(self) -> None:
        """
        send heart beat
        :return:
        """
        def do_beat(instance):

            self.register_dict["healthy"] = self.healthy = int(time.time())
            try:
                re = self.send_heartbeat(instance.service_name, instance.ip, port=instance.port)
                _logger.info(re)
                if (re['code'] != 10200):
                    self.register_dict["healthy"] = int(time.time()) - 10
                    self.__register(instance)

            except:
                self.register_dict["healthy"] = int(time.time()) - 10
                _logger.error("服务心跳维持失败！", exc_info=True)

        map(do_beat, self.Register_already) if len(self.Register_already) > 1 else do_beat(list(self.Register_already)[0])


    def __auto_send_beat(self) -> None:
        while True:
            self.__heart_beat()
            time.sleep(self.__heartbeat_interval)

    #TODO

    def __get_instance_addr(self, service_name):

        """
        调用nacos接口请求，返回可用地址,md5一致则不改变内存中的数据，否则变更新的实例信息
        仅获取
        :param serviceName:
        :param group:
        :param namespaceId:
        :return:
        """
        if service_name not in self.load_balance_dict:
            self.load_balance_dict[service_name] = {}
        try:
            re = self.list_naming_instance(service_name=service_name)
            msg = re['hosts']
            _logger.info(msg)
        except Exception:
            _logger.error("获取实例错误！", exc_info=True)
            msg = []
        hosts = []
        if not msg:
            raise Exception

        for item in msg:
            hosts.append({
                'ip': item['ip'],
                'port': item['port'],
                'healthy': item['healthy']
            })
        hosts_json = json.dumps(hosts)
        md5Content = self.get_md5(hosts_json)
        try:
            oldMd5 = self.load_balance_dict[service_name]["md5"]
        except KeyError:
            self.load_balance_dict[service_name]["md5"] = md5Content
            oldMd5 = ""
        if oldMd5 != md5Content:
            healthy_hosts = list()
            for host in msg:
                healthy_hosts.append(HostsWrapper(**host))
            self.load_balance_dict[service_name]["ip_list"] = healthy_hosts
            self.load_balance_dict[service_name]["index"] = 0
        return hosts


    def __get_and_subscribe_server(self, instance_or_name):
        """
        添加订阅
        :param service_obj:
        :return:
        """
        ret = self.__get_instance_addr(instance_or_name)
        self.subscribe([ListenerBase(instance_or_name, self), ], **{"service_name": instance_or_name})
        return ret


    def add_regist(self, instance):
        """
        手动调用
        :param instance:
        :return:
        """
        self.__register(instance)


    def remove_ins(self, instance):
        """
        手动调用
        :param instance:
        :return:
        """
        self.__deregister(instance)


    def start(self, instance = None) -> None:
        try:
            self.__register(instance)
            self.__heartbeat_timer.start()
        except:
            pass


    def cancel(self) -> None:
        if self.__heartbeat_timer.is_alive():
            self.__heartbeat_timer.cancel()
        self.__deregister()


    def load_balance_client_avr(self, server_name):
        """
        轮询，由index 返回一个IP
        :param instance:
        :return:
        """
        if server_name not in self.load_balance_dict:
            self.__get_and_subscribe_server(server_name)
        index = self.load_balance_dict[server_name]["index"]
        l = len(self.load_balance_dict[server_name]["ip_list"])
        if l == 0:
            _logger.error("无可用服务 serviceName: " + server_name)
            return ""
        if index >= l:
            self.load_balance_dict[server_name]["index"] = 1
            host_obj = self.load_balance_dict[server_name]["ip_list"][0]
        else:
            self.load_balance_dict[server_name]["index"]  = index + 1
            host_obj = self.load_balance_dict[server_name]["ip_list"][index]

        return host_obj.ip_str()


    def get_random_provider(self, server_name):
        """
        根据权重和是否健康获取一个provider
        :param kwargs:
        :return:
        """
        if server_name not in self.load_balance_dict:
            self.__get_and_subscribe_server(server_name)
        service_url_list = [host_obj for host_obj in self.load_balance_dict[server_name]["ip_list"] if host_obj.is_valid]
        if not service_url_list:
            raise NoProvider(data='can not find provider for %s'%server_name)

        total_weight = 0
        same_weight = True
        last_service_url = None
        for host_obj in service_url_list:
            total_weight += host_obj.weight
            if same_weight and last_service_url and last_service_url.weight !=  host_obj.weight:
                same_weight = False
            last_service_url = host_obj

        if total_weight > 0 and not same_weight:
            offset = random.randint(0, total_weight - 1)
            for host_obj in service_url_list:
                offset -= host_obj.weight
                if offset < 0:
                    return host_obj.ip_str()

        return random.choice(service_url_list).ip_str()




__cache_key = "default"
__cache_clients = {}
__cache_clients_lock = RLock()

def init(instance=None) -> JdPyNacosClient:
    """
    Initialize an Client object and put it to cache.
    Unlike using Client class that you need to start and stop the client object by yourself, this method
    will start the client automatically after the object created and stop it when the programe exist.
    read Client for more information for the parameters details.
    :return: client object
    """
    with __cache_clients_lock:
        if __cache_key in __cache_clients:
            _logger.warning("A client is already running, try to stop it and start the new one!")
            __cache_clients[__cache_key].stop()
            del __cache_clients[__cache_key]
        if getattr(instance, 'name_space'):
            na_obj.namespace = instance.name_space
        client = JdPyNacosClient('',server_center=na_obj)
        __cache_clients[__cache_key] = client
        if instance.need:
            client.start(instance)
        return client


def stop() -> None:
    client = get_client()
    if client is not None:
        client.cancel()

def get_client() -> JdPyNacosClient:
    with __cache_clients_lock:
        if __cache_key in __cache_clients:
            return __cache_clients[__cache_key]
        else:
            return None

@atexit.register
def _cleanup_before_exist():
    if len(__cache_clients) > 0:
        _logger.debug("cleaning up clients")
        for k, cli in __cache_clients.items():
            _logger.debug(f"try to stop cache client [{k}] this will also unregister this client from the eureka server")
            cli.cancel()


def client_warpper(method, server_name):
    def get_ip(f):
        def mainPro():
            cli = get_client()
            if not cli:
                return ''
            else:
                # if method is not Callable:
                #     return getattr(cli, method)(server_name)
                return method(server_name)

        mainPro.__name__ = f.__name__
        return mainPro

    return get_ip