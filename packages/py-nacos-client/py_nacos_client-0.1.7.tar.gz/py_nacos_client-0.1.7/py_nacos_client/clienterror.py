#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/26 8:25 下午
# @Author  : lijiarui
# @Email   : lijiarui15@jd.com
# @Site    : 
# @File    : clienterror.py
# @Software: PyCharm
"""
custom exception
"""

nacos_client_error = {}


class NacosClientError(RuntimeError):
    code = None
    message = None
    data = None

    def __init__(self, message=None, data=None, code=None):
        RuntimeError.__init__(self)
        self.message = message or self.message
        self.data = data
        self.code = code
        assert self.code, "Error without code is not allowed"

    def __str__(self):
        return "NacosClientError({code}) : {message}".format(
            code=self.code,
            message=str(self.message)
        )

    def __unicode__(self):
        return u"NacosClientError({code}) : {message}".format(
            code=self.code,
            message=str(self.message)
        )


class NoProvider(NacosClientError):
    code = 5050
    message = u'No provider name {0}'
    provide_name = u''

    def __init__(self, message=None, data=None):
        self.provide_name = data
        NacosClientError.__init__(self, message=self.message.format(data), data=data)


class ConnectionFail(NacosClientError):
    code = 504
    message = u'connect failed {0}'

    def __init__(self, message=None, data=None):
        message = self.message.format(data)
        NacosClientError.__init__(self, message=message, data=data)


class MethodNotFound(NacosClientError):
    code = -601
    message = u'The method does not exist / is not available'

    def __init__(self, message=None, data=None):
        NacosClientError.__init__(self, message=message, data=data)


nacos_client_error[NoProvider.code] = NoProvider
nacos_client_error[ConnectionFail.code] = ConnectionFail
nacos_client_error[MethodNotFound.code] = MethodNotFound
