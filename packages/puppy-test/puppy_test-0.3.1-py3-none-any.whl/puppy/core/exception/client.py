# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: pre processor Exception
"""


class HttpMethodIsNotSupportedException(Exception):
    def __init__(self, error_method):
        self.args = ("当前HTTP客户端不支持此请求方法：{}!".format(error_method),)


class HttpDataIsNotSupportedException(Exception):
    def __init__(self, method, error_type):
        self.args = ("当前HTTP客户端的 {} 方法无法处理 {} 格式的数据!".format(method, error_type),)
