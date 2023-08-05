# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function:format  print debug information
"""
from ..printer.color import Color
from ..function.cfg.config import config


class Printer(object):
    # 前置处理
    __color_of_pre_processor = Color.green_front
    # 默认
    __default = Color.default
    # 后置处理
    __color_of_post_processor = Color.yellow_front
    # 紫色
    __color_of_key_text = Color.purple
    # 格式化输出长度
    __format_str_length = config.get_config("format_str_length", int)

    @classmethod
    def __to_good_text(cls, text):
        """
        得到适合打印的文本
        :param text:
        :return:
        """
        text = str(text)
        if text == "":
            return "空字符串"
        if text is None:
            return None
        # text=text.encode(encoding="utf-8").decode(encoding="raw-unicode-escape")
        if len(text) >= cls.__format_str_length != -1:
            text = "{}......".format(text[:cls.__format_str_length])
        return text

    @classmethod
    def print_pre_processor_start(cls):
        """
        打印开始执行前置处理
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("\ndebug:{}开始执行前置处理器:----------{}".format(cls.__color_of_pre_processor, cls.__default))

    @classmethod
    def print_pre_processor_first(cls, desc, p_type, act):
        """
        打印前置处理器
        :param desc:描述
        :param p_type: 类型
        :param act:动作为
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("\ndebug:执行描述为 {} 的前置处理,".format(desc), end="")
        print("它的数据来源为 {}{}{} ,".format(cls.__color_of_pre_processor, p_type, cls.__default), end="")
        print("动作为 {}{}{} ".format(cls.__color_of_pre_processor, act, cls.__default))

    @classmethod
    def print_pre_processor_getting_data_fail(cls, default):
        """
        打印前置处理器取得数据失败使用默认值的提示
        :param default:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        value = cls.__to_good_text(default)
        print("debug:前置处理器提取结果 {}失败{}，使用默认值 {}{}{}".format(cls.__color_of_pre_processor, cls.__default,
                                                           cls.__color_of_pre_processor, value, cls.__default))

    @classmethod
    def print_pre_processor_second(cls, value):
        """
        打印前置处理器的结果
        :param value:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        type_ = type(value)
        value = cls.__to_good_text(value)
        print("debug:前置处理结果为 {}{}{} ,结果类型为 {} ".format(cls.__color_of_pre_processor, value, cls.__default, type_))

    @classmethod
    def print_pre_processor_n(cls, desc, p_type, act):
        """
        打印不执行的前置处理器
        :param desc:
        :param p_type:
        :param act:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("\ndebug:if属性判断为假 ,不执行", end="")
        print("描述为 {} 的前置处理,".format(desc), end="")
        print("它的类型为 {}{}{} ,".format(cls.__color_of_pre_processor, p_type, cls.__default), end="")
        print("动作为 {}{}{} ".format(cls.__color_of_pre_processor, act, cls.__default))

    @classmethod
    def print_post_processor_start(cls):
        """
        打印开始执行后置处理
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("\ndebug:{}开始执行后置处理器:----------{}".format(cls.__color_of_post_processor, cls.__default))

    @classmethod
    def print_post_processor_first(cls, desc, p_type, act):
        """
        打印后置处理器
        :param desc:描述
        :param p_type: 类型
        :param act:动作为
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("\ndebug:执行描述为 {} 的后置处理,".format(desc), end="")
        print("它的类型为 {}{}{} ,".format(cls.__color_of_post_processor, p_type, cls.__default), end="")
        print("动作为 {}{}{} ".format(cls.__color_of_post_processor, act, cls.__default))

    @classmethod
    def print_post_processor_getting_data_fail(cls, default):
        """
        打印前置处理器取得数据失败使用默认值的提示
        :param default:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        value = cls.__to_good_text(default)
        print("debug:后置处理器提取结果 {}失败{} ，使用默认值 {}{}{}".format(cls.__color_of_post_processor, cls.__default,
                                                            cls.__color_of_post_processor, value, cls.__default))

    @classmethod
    def print_post_processor_second(cls, value):
        """
        打印后置处理器的结果
        :param value:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        type_ = type(value)
        value = cls.__to_good_text(value)
        print("debug:后置处理结果为 {}{}{} ,结果类型为 {} ".format(cls.__color_of_post_processor, value, cls.__default, type_))

    @classmethod
    def print_post_processor_n(cls, desc, p_type, act):
        """
        打印不执行的后置处理器
        :param desc:
        :param p_type:
        :param act:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("\ndebug:if属性判断为假,不执行", end="")
        print("描述为 {} 的后置处理,".format(desc), end="")
        print("类型为 {}{}{} ,".format(cls.__color_of_post_processor, p_type, cls.__default), end="")
        print("动作为 {}{}{} ".format(cls.__color_of_post_processor, act, cls.__default))

    @classmethod
    def print_param_start(cls):
        """
        打印开始执行后置处理
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("\ndebug:{}开始执行参数替换:----------{}".format(cls.__color_of_post_processor, cls.__default))

    @classmethod
    def print_param_replace_first(cls, scope, name):
        """
        参数替换1
        :param scope:
        :param name:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("\ndebug:执行接口信息替换,", end="")
        print("替换 {}{}{} 中的".format(cls.__color_of_pre_processor, scope, cls.__default), end="")
        print(" {}{}{} ".format(cls.__color_of_pre_processor, name, cls.__default))

    @classmethod
    def print_param_replace_second(cls, value):
        """
        参数替换2
        :return:
        """
        if not config.get_config("debug", bool):
            return
        value = cls.__to_good_text(value)
        print("debug:替换为 {}{}{} ".format(cls.__color_of_pre_processor, value, cls.__default))

    @classmethod
    def print_param_replace_first_by_regex(cls, scope, regex, count):
        """
        参数替换1
        :param scope:
        :param regex:
        :param count:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("\ndebug:执行接口信息替换,", end="")
        print("替换 {}{}{} 中的".format(cls.__color_of_pre_processor, scope, cls.__default), end="")
        print("匹配正则表达式 {}{}{} 的".format(cls.__color_of_pre_processor, regex, cls.__default), end="")
        print("第 {}{}{} 个匹配".format(cls.__color_of_pre_processor, str(count), cls.__default), end="")

    @classmethod
    def print_param_delete(cls, scope, name):
        """
        参数替换1
        :param scope:
        :param name:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("\ndebug:执行接口信息删除,", end="")
        print("删除 {}{}{} 中的".format(cls.__color_of_pre_processor, scope, cls.__default), end="")
        print(" {}{}{} ".format(cls.__color_of_pre_processor, name, cls.__default))

    @classmethod
    def print_param_delete_by_regex(cls, scope, regex, count):
        """
        参数替换1
        :param scope:
        :param regex:
        :param count:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("\ndebug:执行接口信息删除,", end="")
        print("删除 {}{}{} 中的".format(cls.__color_of_pre_processor, scope, cls.__default), end="")
        print("匹配正则表达式 {}{}{} 的".format(cls.__color_of_pre_processor, regex, cls.__default), end="")
        print("第 {}{}{} 个匹配".format(cls.__color_of_pre_processor, str(count), cls.__default))

    @classmethod
    def print_param_insert_first(cls, scope, name):
        """
        参数替换1
        :param scope:
        :param name:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("\ndebug:执行接口信息插入,", end="")
        print("在 {}{}{} 中插入参数".format(cls.__color_of_pre_processor, scope, cls.__default), end="")
        print(" {}{}{} ".format(cls.__color_of_pre_processor, name, cls.__default), end="")

    @classmethod
    def print_param_insert_second(cls, value):
        """
        参数替换2
        :return:
        """
        if not config.get_config("debug", bool):
            return
        value = cls.__to_good_text(value)
        print("debug:插入值为 {}{}{} ".format(cls.__color_of_pre_processor, value, cls.__default))

    @classmethod
    def print_assert_first(cls, desc, a_type, act):
        """
        断言器1
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("\ndebug:执行描述为 {} 的断言,".format(desc), end="")
        print("它的类型为 {}{}{} ,".format(cls.__color_of_post_processor, a_type, cls.__default), end="")
        print("动作为 {}{}{} ".format(cls.__color_of_post_processor, act, cls.__default))

    @classmethod
    def print_assert_second(cls, value, expect):
        """
        断言器2
        :param value:
        :param expect:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        value = cls.__to_good_text(value)
        expect = cls.__to_good_text(expect)
        print("debug:实际结果为 {}{}{} ".format(cls.__color_of_post_processor, value, cls.__default))
        print("debug:期望结果为 {}{}{} ".format(cls.__color_of_post_processor, expect, cls.__default))

    @classmethod
    def print_call_method(cls, method_name, *params):
        """
        打印方法调用
        :param method_name:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("debug:调用函数 {}{}{} ".format(cls.__color_of_key_text, method_name, cls.__default))
        for c in range(0, len(params)):
            print("debug:其参数{}: {}{}{} ".format(c + 1, cls.__color_of_key_text, cls.__to_good_text(params[c]),
                                                cls.__default))

    @classmethod
    def print_sql(cls, sql):
        """
        打印sql
        """
        if not config.get_config("debug", bool):
            return
        sql = cls.__to_good_text(sql)
        print("debug:执行sql {}{}{} ".format(cls.__color_of_key_text, sql, cls.__default))

    @classmethod
    def print_sql_res(cls, sql):
        """
        打印sql
        :param sql:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        sql = cls.__to_good_text(sql)
        print("debug:其sql返回的完整结果为 {}{}{} ".format(cls.__color_of_pre_processor, sql, cls.__default))

    @classmethod
    def print_call_method_re(cls, value):
        """
        打印方法调用结果
        :param value:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        value = cls.__to_good_text(value)
        print("debug:其返回结果 {}{}{} ".format(cls.__color_of_key_text, value, cls.__default))

    @classmethod
    def print_if(cls, desc, flag):
        """
        断言器1
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("debug:描述为 {} 的if分支判断为: {}{}{} ".format(desc, cls.__color_of_post_processor, flag, cls.__default))

    @classmethod
    def print_while(cls, desc, flag):
        """
        断言器1
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("debug:描述为 {} 的while循环判断为: {}{}{} ".format(desc, cls.__color_of_post_processor, flag, cls.__default))

    @classmethod
    def print_for_ing(cls, desc, data):
        """
        断言器1
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print(
            "debug:描述为 {} 的for标签正在遍历数据，其数据为: {}{}{} ".format(desc, cls.__color_of_post_processor, data, cls.__default))

    @classmethod
    def print_for_not(cls, desc):
        """
        断言器1
        :return:
        """
        if not config.get_config("debug", bool):
            return
        print("debug:描述为 {} 的for标签其数据项为空，无需遍历".format(desc))

    @classmethod
    def print_set(cls, name, value):
        """
        打印processor中set标签的值
        :param name:
        :param value:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        type_ = type(value)
        value = cls.__to_good_text(value)
        print("debug:接口处理标签set变量到局部变量池:变量名为 {} ,变量值为 {} ,类型为 {} ".format(name, value, type_))

    @classmethod
    def print_sql_for_set(cls, name, value, default=False):
        """
        打印processor中sql标签设置的变量
        :param name:
        :param value:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        type_ = type(value)
        value = cls.__to_good_text(value)
        if default:
            print("debug:接口处理标签sql设置变量到局部变量池:变量名为 {} ,使用默认变量值为 {} ,类型为 {} ".format(name, value, type_))
        else:
            print("debug:接口处理标签sql设置变量到局部变量池:变量名为 {} ,变量值为 {} ,类型为 {} ".format(name, value, type_))

    @classmethod
    def print_sleep(cls, time):
        """
        打印睡眠的时间
        :return:
        """
        if not config.get_config("debug", bool):
            return
        value = "debug:睡眠 {} 秒".format(str(time))
        value = cls.__to_good_text(value)
        print(value)


if __name__ == '__main__':
    Printer.print_param_replace_first("ddd", "ddd")
