# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: client
"""
import abc
from copy import deepcopy
from .... import config
from ....api.common.res_data import ResData
from ....api.process.post import PostProcessor
from ....api.process.pre import PreProcessor
from ....data.interface import Interface


class AbstractClient(metaclass=abc.ABCMeta):

    def __init__(self, interface_info: Interface, interface_data: dict, context: dict):
        """
        客户端
        :param interface_info: 接口信息
        :param interface_data: 接口数据
        :param context: 上下文
        """
        # 场景上下稳
        self._context = context
        # 测试数据
        self._interface_data = interface_data
        # 接口信息
        self._interface_info = deepcopy(interface_info)
        # 数据库链接字符串
        self._db_info = self._interface_data.get("db_info")
        # 前置处理器数据
        self._pre_data = self._interface_data.get("pre_processor")
        # 后置处理器数据
        self._post_data = self._interface_data.get("post_processor")
        # 结果
        self._res = ResData()

    @abc.abstractmethod
    def _request(self):
        pass

    def request(self):
        # 如果有前置处理器进行前置处理
        if self._pre_data:
            if self._db_info is not None:
                if self._pre_data.get("db_info") is None:
                    self._pre_data["db_info"] = self._db_info
            PreProcessor(self._interface_data, self._interface_info, self._pre_data).work(self._context)
        # 判断是否存在expect
        if config.get_config("the_global_inspection",bool) and (
                self._post_data is None or "expect" not in self._post_data):
            raise Exception("接口必须包含至少一个断言！")
        # 发送请求
        self._request()
        # 如果有后置处理器进行后置处理
        if self._post_data:
            if self._db_info is not None:
                if self._post_data.get("db_info") is None:
                    self._post_data["db_info"] = self._db_info
            PostProcessor(self._interface_data, self._interface_info, self._post_data, self._res).work(
                self._context)
