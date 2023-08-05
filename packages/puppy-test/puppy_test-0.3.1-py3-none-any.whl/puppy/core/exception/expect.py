# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: expect exception
"""


class ExpectDescIsNullException(Exception):
    def __init__(self) -> None:
        self.args = ("期望标签的描述不能为空！",)


class ExpectKeyTypeIsIncorrectException(Exception):
    def __init__(self, expect_desc: str, key: str):
        self.args = ("期望标签的key错误,当结果类型是二维表数据时,key应是数字切片的格式,类似'1:2',不应是:{},此期望标签描述为:{}".format(key, expect_desc),)


class ExpectActIsNullException(Exception):
    def __init__(self, expect_desc: str) -> None:
        self.args = ("期望标签未指定指定动作,该期望标签的描述为:{}".format(expect_desc),)


class ExpectSqlIsNullException(Exception):
    def __init__(self, expect_desc: str) -> None:
        self.args = ("期望标签未指定指定要执行的sql语句,该期望标签的描述为:{}".format(expect_desc),)


class ExpectValueIsNullException(Exception):
    def __init__(self, expect_desc: str) -> None:
        self.args = ("期望标签未指定指定期望值,该期望标签的描述为:{}".format(expect_desc),)


class ExpectTypeIsUnsupportedException(Exception):
    def __init__(self, expect_desc, type_):
        self.args = ("期望标签的类型不正确，不支持：{}，该期望标签的描述为:{}".format(type_, expect_desc),)


class ExpectReTypeUnsupportedException(Exception):
    def __init__(self, expect_desc, type_):
        self.args = ("期望标签不支持对 {} 类型的结果进行处理，该期望标签的描述为:{}".format(type_, expect_desc),)


class ExpectJsonException(Exception):
    def __init__(self, expect_desc: str, error_json: str):
        self.args = ("期望标签处理的数据不是正确的json格式字符串：{}，该期望标签的描述为:{}".format(error_json, expect_desc),)


class ExpectActIsUnsupportedException(Exception):
    def __init__(self, expect_desc: str, act: str):
        self.args = ("期望标签不支持此动作:{}，该期望标签的描述为:{}".format(act, expect_desc),)

class ExpectValueIsNullException(Exception):
    def __init__(self,expect_desc:str):
        self.args=("期望标签的type是expression时，其value不能为空，该期望标签的描述为:{}".format(expect_desc),)
