# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: interface Exception
"""


class InfNameIsNullException(Exception):
    def __init__(self, scope):
        self.args = (" {} 标签的name不能为空！".format(scope),)


class InfFileNameIsIncorrectException(Exception):
    def __init__(self, scope, error_name):
        self.args = (" {} 标签的name {} 是不正确的,不能是正则表达式或$whole".format(scope, error_name),)


class InfPortAndServerNameIsIncorrectException(Exception):
    def __init__(self, scope, error_name):
        self.args = (" {} 标签的name {} 是不正确的,只能是$whole".format(scope, error_name),)


class InfActIsIncorrectException(Exception):
    def __init__(self, scope, error_act):
        self.args = (" {} 标签的act {} 是不正确的，只能是delete,replace,insert".format(scope, error_act),)


class InfValueIsNotNoneException(Exception):
    def __init__(self, scope, act, name):
        if name == "$Regex":
            name = "正则表达式"
        self.args = ("由于name为{} 的 {} 标签的act是 {} ,其标签值不能为空!".format(name, scope, act),)


class InfDataIsNotMatchedException(Exception):
    def __init__(self, scope, regex, inf_name, inf_data):
        self.args = (
            " {} 标签处理出错，接口 {} 的 {} 与 正则表达式 {} 匹配失败\n待匹配字符串为 {} ".format(scope, inf_name, scope, regex, inf_data),)


class InfDataNotContainsTheWellException(Exception):
    def __init__(self, scope, well, inf_name, inf_data):
        self.args = (
            " {} 标签处理出错，接口 {} 的 {} 中 {} 不包含 {} ".format(scope, inf_name, scope, inf_data, well),)


class InfDataNotSupportException(Exception):
    def __init__(self, scope, inf_name, act):
        self.args = (
            " {} 标签处理出错，接口 {} 的 {} 不支持name为#表达式进行 {} 动作 ".format(scope, inf_name, scope, act),)


class InfIsNotFileException(Exception):
    def __init__(self, scope, inf_name):
        self.args = (" {} 标签处理出错，接口 {} 不是一个文件上传接口！".format(scope, inf_name),)


class InfReTypeIsUnsupportedException(Exception):
    def __init__(self, scope, ty):
        self.args = (" {} 标签处理出错，不支持对类型为 {} 的数据进行处理！".format(scope, ty),)


class InfDataIsNotFindException(Exception):
    def __init__(self, scope, key, inf_name):
        self.args = (" {} 标签处理出错，接口 {} 的 {} 不存在关键字 {} 或关键字格式错误".format(scope, inf_name, scope, key),)


class InfDataIsIncorrectException(Exception):
    def __init__(self, scope, inf_name):
        self.args = (" {} 标签处理出错，接口 {} 的 {} 格式不正确，请检查！".format(scope, inf_name, scope),)


class InfInsertFailException(Exception):
    def __init__(self, scope, inf_name, insert_key, value):
        self.args = (
            " {} 标签处理出错，在接口 {} 的 {} 中插入参数 {} 失败，因为参数格式不正确，其待插入的值为 {}".format(scope, inf_name, scope, insert_key,
                                                                             value),)
