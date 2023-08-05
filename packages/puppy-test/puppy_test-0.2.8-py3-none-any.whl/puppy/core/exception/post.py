# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: post processor exception
"""


class PostTypeIsIncorrectException(Exception):
    def __init__(self, post_desc: str, error_type: str) -> None:
        self.args = ("后置处理器不支持此type:{},该后置处理器的描述为:{}".format(error_type, post_desc),)


class PostDescIsNullException(Exception):
    def __init__(self) -> None:
        self.args = ("后置处理器的描述不能为空！",)


class PostKeyTypeIsIncorrectException(Exception):
    def __init__(self, post_desc: str, key: str):
        self.args = ("后置处理器的key错误,当结果类型是二维表数据时,key应是数字切片的格式,类似'1:2',不应是:{},此后置处理器描述为:{}".format(key, post_desc),)


class PostActIsIncorrectException(Exception):
    def __init__(self, post_desc: str, act: str):
        self.args = ("后置处理器的act错误,不能是:{},该后置处理器的描述为:{}".format(act, post_desc),)


class PostVarTypeIsNotSupportException(Exception):
    def __init__(self, post_desc: str, type_: str):
        self.args = ("后置处理器的var_type不受支持,不能是:{},该后置处理器的描述为:{}".format(type_, post_desc),)


class PostNameIsNotSupportedException(Exception):
    def __init__(self, post_desc: str, name: str):
        self.args = ("后置处理器的name不符合规则,只能以字母下划线开头且只包含字母数字下划线,不能是:{},该后置处理器的描述为:{}".format(name, post_desc),)


class PostNameIsNullException(Exception):
    def __init__(self, post_desc: str):
        self.args = ("后置处理器是set型的处理器时的name不能是空,该后置处理器的描述为:{}".format(post_desc),)


class PostValueIsNotSpecifiedException(Exception):
    def __init__(self, post_desc: str):
        self.args = ("后置处理器的value或type未指定,该后置处理器的描述为:{}".format(post_desc),)


class PostSqlIsNotSpecifiedException(Exception):
    def __init__(self, post_desc: str):
        self.args = ("后置处理器未配置sql语句,该后置处理器的描述为:{}".format(post_desc),)


class PostExpressIsIncorrectException(Exception):
    def __init__(self, post_desc: str, error: str):
        self.args = ("描述为 {} 后置处理器的ex计算出错，错误原因时为:{}".format(post_desc, error),)


class PostNotFindValueException(Exception):
    def __init__(self, post_desc: str, res_type: str, key: str):
        self.args = ("后置处理器未在结果 {} 中找到关键字为 {} 或关键字格式不正确，该后置处理器的描述为：{}".format(res_type, key, post_desc),)


class PostReTypeIsNotSupportedException(Exception):
    def __init__(self, post_desc: str, re_type: str):
        self.args = ("后置处理器不支持处理此种类型的结果:{},该后置处理器的描述为:{}".format(re_type, post_desc),)


class PostReqDataIsNullException(Exception):
    def __init__(self, post_desc):
        self.args = ("后置处理器无法处理请求报文，因为该接口的请求报文为空，该后置处理器的描述为:{}".format(post_desc),)


class PostSleepValueIsNotNumberException(Exception):
    def __init__(self, post_desc: str, value: str):
        self.args = ("sleep型的后置处理器传入的结果值必须一个数字，而不是：{}，该后置处理器的描述为：{}".format(value, post_desc),)


class PostTransferFailException(Exception):
    def __init__(self, post_desc: str, value: str, type_: str):
        self.args = ("后置处理器取到的数据 {} 不是 {} 类型，转型失败，该后置处理器的描述为:{}".format(value, type_, post_desc),)


class PostValueAndExceptValueIsNotSameException(Exception):
    def __init__(self, post_desc: str, real: str, except_v: str):
        self.args = ("后置处理器取到的值 {} 与处理器value说明的值 {} 不一致，该处理器的描述为:{}".format(real, except_v, post_desc),)


class PostValueAndExceptValueIsNotMatchedException(Exception):
    def __init__(self, post_desc: str, real: str, regex: str):
        self.args = ("后置处理器取到的值 {} 与处理器value说明的正则表达式 {} 不匹配，该处理器的描述为:{}".format(real, regex, post_desc),)


class PostValueTypeIsNotCorrectException(Exception):
    def __init__(self, post_desc: str, value, _type):
        self.args = ("后置处理器取到的值 {} 类型 {} 不正确，当需要设置多个变量时，值的类型必须是列表或tuple，该处理器的描述为:{}".format(value, _type, post_desc),)


class PostValueLengthIsNotCorrectException(Exception):
    def __init__(self, post_desc: str, need_length, real_length):
        self.args = ("后置处理器取需要的变量数:{}个与实际得到的变量数:{}个不等，该处理器的描述为:{}".format(need_length, real_length, post_desc),)
