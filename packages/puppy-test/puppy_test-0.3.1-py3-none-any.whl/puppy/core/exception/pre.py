# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: pre processor exception
"""


class PreTypeIsIncorrectException(Exception):
    def __init__(self, pre_desc: str, error_type: str) -> None:
        self.args = ("前置处理器不支持此type:{},该前置处理器的描述为:{}".format(error_type, pre_desc),)


class PreDescIsNullException(Exception):
    def __init__(self) -> None:
        self.args = ("前置处理器的描述不能为空！",)


class PreKeyTypeIsIncorrectException(Exception):
    def __init__(self, pre_desc: str, key: str):
        self.args = ("前置处理器的key错误,当结果类型是二维表数据时,key应是数字切片的格式,类似'1:2',不应是:{},此前置处理器描述为:{}".format(key, pre_desc),)


class PreActIsIncorrectException(Exception):
    def __init__(self, pre_desc: str, act: str):
        self.args = ("前置处理器的act错误,不能是:{},该前置处理器的描述为:{}".format(act, pre_desc),)


class PreVarTypeIsNotSupportException(Exception):
    def __init__(self, pre_desc: str, type_: str):
        self.args = ("前置处理器的var_type不受支持,不能是:{},该前置处理器的描述为:{}".format(type_, pre_desc),)


class PreNameIsNotSupportedException(Exception):
    def __init__(self, pre_desc: str, name: str):
        self.args = ("前置处理器的name不符合规则,只能以字母下划线开头且只包含字母数字下划线,不能是:{},该前置处理器的描述为:{}".format(name, pre_desc),)


class PreNameIsNullException(Exception):
    def __init__(self, pre_desc: str):
        self.args = ("前置处理器是set型的处理器时的name不能是空,该前置处理器的描述为:{}".format(pre_desc),)


class PreValueIsNotSpecifiedException(Exception):
    def __init__(self, pre_desc: str):
        self.args = ("前置处理器的value或type未指定,该前置处理器的描述为:{}".format(pre_desc),)


class PreSqlIsNotSpecifiedException(Exception):
    def __init__(self, pre_desc: str):
        self.args = ("前置处理器未配置sql语句,该前置处理器的描述为:{}".format(pre_desc),)


class PreExpressIsIncorrectException(Exception):
    def __init__(self, pre_desc: str, error: str):
        self.args = ("描述为 {} 的前置处理器的表达式计算错误，原因为:{}".format(pre_desc, error),)


class PreNotFindValueException(Exception):
    def __init__(self, pre_desc: str, res_type: str, key: str):
        self.args = ("前置处理器未在结果 {} 中找到关键字为 {} 或关键字格式不正确，该前置处理器的描述为：{}".format(res_type, key, pre_desc),)


class PreReTypeIsNotSupportedException(Exception):
    def __init__(self, pre_desc: str, re_type: str):
        self.args = ("前置处理器不支持处理此种类型的结果:{},该前置处理器的描述为:{}".format(re_type, pre_desc),)


class PreReqDataIsNullException(Exception):
    def __init__(self, pre_desc):
        self.args = ("前置处理器无法处理请求报文，因为该接口的请求报文为空，该前置处理器的描述为:{}".format(pre_desc),)


class PreSleepValueIsNotNumberException(Exception):
    def __init__(self, pre_desc: str, value: str):
        self.args = ("sleep型的前置处理器传入的结果值必须一个数字，而不是：{}，该前置处理器的描述为：{}".format(value, pre_desc),)


class PreTransferFailException(Exception):
    def __init__(self, pre_desc: str, value: str, type_: str):
        self.args = ("前置处理器取到的数据 {} 不是 {} 类型，转型失败，该前置处理器的描述为:{}".format(value, type_, pre_desc),)


class PreValueAndExceptValueIsNotSameException(Exception):
    def __init__(self, pre_desc: str, real: str, except_v: str):
        self.args = ("前置处理器取到的值 {} 与处理器value说明的值 {} 不一致，该处理器的描述为:{}".format(real, except_v, pre_desc),)


class PreValueAndExceptValueIsNotMatchedException(Exception):
    def __init__(self, pre_desc: str, real: str, regex: str):
        self.args = ("前置处理器取到的值 {} 与处理器value说明的正则表达式 {} 不匹配，该处理器的描述为:{}".format(real, regex, pre_desc),)


class PreValueTypeIsNotCorrectException(Exception):
    def __init__(self, post_desc: str, value, _type):
        self.args = ("前置处理器取到的值 {} 类型 {} 不正确，当需要设置多个变量时，值的类型必须是列表或tuple，该处理器的描述为:{}".format(value, _type, post_desc),)


class PreValueLengthIsNotCorrectException(Exception):
    def __init__(self, post_desc: str, need_length, real_length):
        self.args = ("前置处理器取需要的变量数:{}个与实际得到的变量数:{}个不等，该处理器的描述为:{}".format(need_length, real_length, post_desc),)
