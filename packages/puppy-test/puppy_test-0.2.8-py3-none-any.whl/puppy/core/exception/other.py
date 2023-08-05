# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: if tag exception
"""


class IFExpressIncorrectException(Exception):
    def __init__(self, if_desc: str, error: str):
        self.args = ("描述为 {} 的if标签的表达式计算错误，具体错误原因为:{}".format(if_desc, error),)


class IFDescIsNullException(Exception):
    def __init__(self):
        self.args = ("if标签的描述不能为空！",)


class UnexpectedTagsException(Exception):
    def __init__(self):
        self.args = ("存在不应存在的标签，请检查！",)


class FileIsNotExistsException(Exception):
    def __init__(self, file):
        self.args = ("文件 {} 不存在，请检查！".format(file),)


class ReqDataIsIncorrectException(Exception):
    def __init__(self):
        self.args = ("请求报文格式不正确，请检查！",)
