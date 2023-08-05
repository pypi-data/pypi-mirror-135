# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: process api scene
"""
import re
import time
from copy import deepcopy
from .client.http import HTTP
from .client.sql import SQL
from .client.tcp import TCP
from ...function.cookies.cookie import CookiesUtils
from ...function.parse.table_parse import TableParse
from ...function.selenium_.selenium_ import Selenium_
from ...function.utils.utils import Utils
from ... import config
from ...data import interface, flow
from ...function.express.express import Express, ParamType
from ...function.thread.pool import ResourcePool
from ...printer.color import Color
from ...printer.debug_printer import Printer
from ...printer.format_printer import Printer as FormatPrinter
from ...printer.logger import Logger


class Processor(object):
    """
    API处理器，用来处理一系列API测试
    """
    # 默认
    __default = Color.default
    # 红前景
    __color_of_title = Color.red_front

    __name_re = re.compile(r"[\w_][\w_\d]*")

    def __init__(self, test_data: dict):
        """
        API处理器，用来处理一系列API测试
        :param test_data: 测试数据字典
        :return:
        """
        # 测试数据
        self.__test_data = test_data
        # 用例id
        if "id" not in self.__test_data:
            raise Exception("案例的id不能为空！")
        self.__case_id = self.__test_data.pop("id")
        # 用例name
        if "name" not in self.__test_data:
            raise Exception("案例的id不能为空！")
        self.__case_name = self.__test_data.pop("name")
        # db_info信息
        self.__db_info = self.__test_data.pop("db_info") if "db_info" in self.__test_data else None
        # 局部变量池
        self.__context = dict()
        # 用来记录层级的顺序
        self.__order = 0
        # session
        self.__session = None
        # 记录嵌套的flow数量
        self.__flow = 0
        # 记录break的状态
        self.__break = False
        # 记录continue的状态
        self.__continue = False
        # 记录嵌套的for或while的数量
        self.__cycle = 0
        # 记录返回
        self.__return = False
        # 用来存储层级式打印的序号堆栈
        self.__number_list = list()
        # 判断是否调用了interface
        self.__invoke_interface = False

    def start(self):
        """
        开始处理场景测试
        :return:
        """
        try:
            # 开始处理
            config.test("{}、{}".format(self.__case_id, self.__case_name))
            print("场景执行：编号：{} 名称：{}++++++++++++++++++++++++++++++++++++".format(self.__case_id, self.__case_name))
            # Logger().logger.info("正在执行名称为：{}{}的案例".format(self.__case_id,self.__case_name))
            self.__process_core(self.__test_data, self.__context)
            print("++++++++++++++++++++++++++++++++++++场景结束：编号：{} 名称：{}".format(self.__case_id, self.__case_name))
        except Exception:
            raise
        finally:
            if self.__session:
                self.__session.close()
            if config.get_config("single_testing", bool):
                ResourcePool().close()

    def __process_core(self, cases, context):
        """
        由处理核心来完成接口的调用
        :param cases:
        :param 上下文环境
        :return:
        """
        # 取得排序后的数据
        sorted_data = Utils.merge_and_sort(cases, Utils.MAIN_TAG)
        for data in sorted_data:
            # 判断一下循环数量是否不为0，break和continue是否为true
            if self.__cycle != 0 and (self.__break or self.__continue):
                return
            # 取得data的名字
            name = data.get("name")
            if self.__flow != 0 and self.__return and name != "return":
                return
            value = data.get("value")
            # 如果是name是if交给if处理
            if name == "if":
                self.__before()
                self.__process_if(value, context)
                self.__after()
            elif name == "break" and self.__cycle != 0:
                self.__break = True
            elif name == "continue" and self.__cycle != 0:
                self.__continue = True
            # 如果name是while交给while处理
            elif name == "while":
                self.__before()
                self.__cycle += 1
                self.__process_while(value, context)
                self.__cycle -= 1
                self.__after()
            # 如果name是set交给set处理
            elif name == "set":
                self.__process_set(value, context)
            elif name == "sql":
                self.__process_sql(value, context)
            # 如果那么是ref交给return处理
            elif name == "flow":
                self.__before()
                self.__flow += 1
                self.__process_flow(value, context)
                self.__flow -= 1
                self.__after()
            # 如果是return交给return处理
            elif name == "return":
                # 将return标志置为真
                self.__return = True
                self.__process_return(value, context)
            elif name == "for":
                self.__before()
                self.__cycle += 1
                self.__process_for(value, context)
                self.__cycle -= 1
                self.__after()
            elif name == "selenium":
                self.__process_selenium(value, context)
            # 如果name是interface交给interface处理
            elif name == "sleep":
                self.__process_sleep(value, context)
            else:
                self.__order += 1
                self.__invoke_interface = True
                self.__process_interface(value, context)

    def __process_flow(self, data, context):
        """
         处理参考标签
        :param data:
        :param context:
        :return:
        """
        # 读取要使用流程的name名
        flow_name = data.get("name")
        # 取到要使用流程flow
        flow_ = flow.get(flow_name)
        # 构造一个局部变量池
        flow_context = deepcopy(flow_.params)
        # 取到流程的实参,并将实参和形参合并
        for key, value in data.items():
            if key not in ["set", "$order", "name"]:
                if key not in flow_.params.keys():
                    raise Exception("[{}]流程中不含有参数名为[{}]的参数，请检查!".format(flow_name, key))
                flow_context[key] = Express.calculate_str(value, context)
        # 将流程交给core处理
        self.__process_core(flow_.content, flow_context)
        if self.__return:
            self.__return = False
        # 处理结束，读取set标签
        sets = data.get("set")
        if type(sets) == dict:
            sets = [sets]
        if sets is not None:
            # 处理set标签
            for i in range(len(sets)):
                if "${}".format(str(i)) not in flow_context.keys():
                    raise Exception("[{}]流程没有足够多的返回值来满足流程调用的set标签！".format(flow_name))
                name = sets[i].get("name")
                context[name] = flow_context["${}".format(str(i))]

    def __process_return(self, data, context):
        """
        处理return
        :param context:
        :return:
        """
        if self.__flow <= 0:
            raise Exception("案例xml中不能包含return标签！")
        # 取到value
        value = data.get("value") if data.get("value") is not None else data.get("$value")
        # 计算value的实际值
        value = Express.calculate_str(value, context)
        # 将value值放入上下文，键设置为
        # 从上下文中读取以$开头后面跟数字的元素，取到该元素的下一个数字
        count = -1
        while True:
            count += 1
            if "${}".format(str(count)) in context.keys():
                continue
            break
        # 将该值放入到上下文，取名$加上count
        context["${}".format(str(count))] = value

    def __process_if(self, data, context):
        """
        处理data数据if
        :param data:
        :return:
        """
        # 取到ex，如果ex计算的值是一个假值，则不执行
        ex = data.get("ex")
        desc = data.get("desc")
        ex_o = Express(ex)
        r = ex_o.calculate(context)
        if r == Utils.ERROR:
            raise Exception("描述为 {} 的if的表达式计算出错，原因为：{}".format(desc, ex_o.error))
        Printer.print_if(desc, r)
        if r:
            self.__process_core(data, context)

    def __process_while(self, data, context):
        """
        处理while
        :param data:
        :return:
        """
        # while需要增加一个执行次数，如果这个实际的执行次数超过了这个次数，将抛出异常
        ex = data.get("ex")
        desc = data.get("desc")
        count = 10 if data.get("count") is None else int(data.get("count"))
        t = 0
        r = None
        while t < count:
            ex_o = Express(ex)
            r = ex_o.calculate(context)
            if r == Utils.ERROR:
                raise Exception("描述为 {} 的while的表达式计算出错，原因为：{}".format(desc, ex_o.error))
            Printer.print_while(desc, r)
            if not r:
                break
            t += 1
            self.__process_core(data, context)
            if self.__break:
                self.__break = False
                break
            if self.__continue:
                self.__continue = False
                continue
        if r:
            raise Exception("while结构已经执行了指定的次数[{}],但还未返回需要的结果".format(count))

    def __process_interface(self, data, context):
        # 清理上下文中的请求和响应信息
        new_session = True if data.get("session") == "new" else False
        Processor.__clear_context_with_res_and_req(context)
        # 取得接口名称
        print("{}-------------{}）接口:{} 描述:{}-------------{}".format(self.__color_of_title,
                                                                    self.__get_print_number(),
                                                                    data.get("name"),
                                                                    data.get("desc"),
                                                                    self.__default))
        if data.get("db_info") is None:
            data["db_info"] = self.__db_info
        else:
            data["db_info"] = Express.calculate_str(data.get("db_info"), context)
        name = data.get("name")
        # 到接口数据中获取对应接口信息
        interface_ = interface.get(name)
        # 根据接口类型选择对应的客户端
        if interface_.protocol in ["http", "https"]:
            if self.__session and not new_session:
                http = HTTP(interface_, data, context, self.__session)
            else:
                if self.__session:
                    self.__session.close()
                http = HTTP(interface_, data, context)
                self.__session = http.session
            http.request()
        elif interface_.protocol == "tcp":
            tcp = TCP(interface_, data, context)
            tcp.request()
        elif interface_.protocol == "sql":
            sql = SQL(interface_, data, context)
            sql.request()
        else:
            raise Exception("暂不支持该种协议：{}".format(interface_.protocol))

    def __get_print_number(self):
        """
        得到可打印的序号
        :return:
        """
        number = ""
        for _ in self.__number_list:
            number += str(_) + "."
        return number + str(self.__order)

    def __process_set(self, data, context):
        """
        处理set标签
        """
        name = data.get("name")
        value = data.get("value") if data.get("value") is not None else data.get("$value")
        var_type = data.get("var_type")
        # 取得真正的name和返回类型
        if name is None or "" == name:
            raise Exception("set标签必须指定name值")
        if value is None:
            raise Exception("name为【{}】的set标签的value参数不能为空".format(name))
        # 判断类型是否符合要求
        if var_type not in ["str", "int", "float", "bool", "auto", None]:
            raise Exception("name为【{}】的set标签的变量还不支持[{}]数据类型".format(name, var_type))
        if "," in name:
            names = name.split(",")
            names = list(map(lambda x: x.strip(), names))
        else:
            names = [name.strip()]
        for n in names:
            if not self.__name_re.fullmatch(n):
                raise Exception("name为【{}】的set标签的变量名称 {} 不符合规则，只能以字母下划线开头且只包含字母数字下划线".format(name, n))
        # 计算获得实际值
        value = Express.calculate_str(value, context)
        if len(names) > 1:
            if type(value) not in [list, tuple]:
                raise Exception(
                    "name为【{}】的set标签取到的值 {} 类型 {} 不正确，当需要设置多个变量时，值的类型必须是列表或元祖".format(name, value, type(value)))
            if len(names) != len(value):
                raise Exception("name为【{}】的set标签需要的变量数:{}个与实际得到的变量数:{}个不等".format(name, len(names), len(value)))
            for i in range(len(names)):
                context[names[i]] = Processor.__get_specified_type_var(value[i], var_type)
                Printer.print_set(names[i], value[i])
        else:
            context[names[0]] = Processor.__get_specified_type_var(value, var_type)
            Printer.print_set(names[0], value)

    @staticmethod
    def __process_sleep(data, context):
        """
        处理sleep标签
        """
        value = data.get("time") if data.get("time") is not None else data.get("$value")
        # 计算获得实际值
        value = Express.calculate_str(value, context)
        try:
            wait = int(value)
        except Exception:
            raise Exception("睡眠的值必须是可转为数字的值，不能是 {} ！".format(value))
        Printer.print_sleep(wait)
        time.sleep(wait)

    def __process_sql(self, data, context):
        """处理sql标签"""
        sql = data.get("sql")
        if sql is None:
            raise Exception("sql标签必须指定sql属性！")
        sql = Express.calculate_sql(sql, context)
        name = data.get("name")
        key = "$whole" if data.get("key") is None else data.get("key")
        var_type = data.get("var_type")
        value = data.get("value") if data.get("value") is not None else data.get("$value")
        # 判断类型是否符合要求
        if var_type not in ["str", "int", "float", "bool", "auto", None]:
            raise Exception("sql标签设置的变量还不支持[{}]数据类型".format(var_type))
        db_info = self.__db_info if data.get("db_info") is None else Express.calculate_str(data.get("db_info"), context)
        res = ResourcePool().exec_sql(db_info, sql)
        Printer.print_sql(sql)
        Printer.print_sql_res(res.res)
        default = False
        if name is not None:
            if "," in name:
                names = name.split(",")
                names = list(map(lambda x: x.strip(), names))
            else:
                names = [name.strip()]
            for n in names:
                if not self.__name_re.fullmatch(n):
                    raise Exception("sql标签的变量名称 {} 不符合规则，只能以字母下划线开头且只包含字母数字下划线".format(n))
            if key == "$whole":
                _v = TableParse(res.res).get_value(key)
            elif key == "$rows":
                _v = res.rows
            elif key == "$columns":
                _v = res.columns
            else:
                _v = TableParse(res.res).get_value(key)
                if _v is Utils.ERROR:
                    if value is None:
                        raise Exception("sql标签未提取到变量值，可能是指定的key格式不正确或错误！\n该sql执行结果为 {}".format(res.res))
                    else:
                        default = True
                        _v = Express.calculate_str(value, context)
            if len(names) > 1:
                if type(_v) not in [list, tuple]:
                    raise Exception(
                        "sql标签取到的值 {} 类型 {} 不正确，当需要设置多个变量时，值的类型必须是列表或元祖".format(_v, type(_v)))
                if len(names) != len(_v):
                    raise Exception("sql标签需要的变量数:{}个与实际得到的变量数:{}个不等".format(len(names), len(_v)))
                for i in range(len(names)):
                    context[names[i]] = Processor.__get_specified_type_var(_v[i], var_type)
                    Printer.print_sql_for_set(names[i], _v[i], default)
            else:
                context[names[0]] = Processor.__get_specified_type_var(_v, var_type)
                Printer.print_sql_for_set(names[0], _v, default)

    def __process_for(self, data, context):
        """
        遍历数据
        :param data:
        :param context:
        :return:
        """
        items = Express.calculate_str(data.get("items"), context)
        desc = data.get("desc")
        if type(items) not in [dict, list, tuple]:
            raise Exception("描述为[{}]的for标签仅能遍历字典、列表、元祖，不可遍历：{}".format(desc, type(items)))
        key = data.get("key")
        key_len = len(key.split(","))
        if type(items) == dict and key_len != 2:
            raise Exception("描述为[{}]的for标签遍历字典时，必须提供两个key，且用英文逗号分开".format(desc))
        if type(items) in [list, tuple] and key_len != 1:
            raise Exception("描述为[{}]的for标签遍历列表，元祖时，仅需提供一个key".format(desc))
        if type(items) == dict:
            keys = key.split(",")
            if len(items.items()) > 0:
                # 拷贝一个上下文
                new_context = deepcopy(context)
                for k, v in items.items():
                    Printer.print_for_ing(desc, "{}<-{},{}<-{}".format(str(keys[0]), str(k), str(keys[1]), str(v)))
                    new_context[keys[0]] = k
                    new_context[keys[1]] = v
                    self.__process_core(data, new_context)
                # 完成后移除变量
                del new_context[keys[0]]
                del new_context[keys[1]]
                context.update(new_context)
            else:
                Printer.print_for_not(desc)
        if type(items) in [list, tuple]:
            if len(items) > 0:
                # 拷贝一个上下文
                new_context = deepcopy(context)
                for v in items:
                    Printer.print_for_ing(desc, "{}<-{}".format(str(key), str(v)))
                    new_context[key] = v
                    self.__process_core(data, new_context)
                    if self.__break:
                        self.__break = False
                        break
                    if self.__continue:
                        self.__continue = False
                        continue
                del new_context[key]
                context.update(new_context)
            else:
                Printer.print_for_not(desc)

    def __process_selenium(self, data, context):
        """
        执行selenium标签
        :param data:
        :param context:
        :return:
        """
        # 取到相关参数
        desc = data.get("desc")
        FormatPrinter.print_info("执行描述为 {} 的selenium操作".format(desc))
        module = data.get("module")
        if not Selenium_.is_exists_the_module(module):
            raise Exception("描述为 {} 的selenium标签的模块名 {} 不存在".format(desc, module))
        func = data.get("func")
        if not Selenium_.is_exists_the_func(module, func):
            raise Exception("描述为 {} 的selenium标签、模块名为 {} 的函数 {} 不存在".format(desc, module, func))
        browser = data.get("browser")
        driver_path = data.get("driver")
        block_cookie = data.get("block_cookie")
        if block_cookie == "True":
            session = None
        else:
            session = self.__session
        # 取到执行参数
        params = data.get("param")
        if type(params) == dict:
            params = [params]
        real_params = dict()
        if params is not None:
            # 处理参数
            for param in params:
                name = param.get("name")
                value = Express.calculate_str(param.get("$value"), context)
                real_params[name] = value
        driver = None
        err = None
        ret = None
        # 创建selenium
        try:
            # 创建selenium对象
            s = Selenium_(module, func, browser, driver_path)
            # 构造driver
            driver = s.make_driver(session)
            # 执行对应功能
            ret = s.execute(driver, **real_params)
            # 执行完成后合并cookie
            if block_cookie != "True":
                self.__session = CookiesUtils.merge_selenium_to_requests(driver, self.__session)
        except Exception as e:
            err = str(e)
        finally:
            if driver:
                driver.quit()
            if err is not None:
                raise Exception("描述为 {} 的selenium标签，执行模块 {} 中的 {} 函数出错，原因为 {} ".format(desc, module, func, err))
        # 处理结束，读取set标签
        set_ = data.get("set")
        if set_ is not None:
            name = set_.get("name")
            context[name] = ret

    def __before(self):
        """
        在嵌套结构调用前
        :return:
        """
        self.__invoke_interface = False
        self.__order += 1
        self.__number_list.append(self.__order)
        self.__order = 0

    def __after(self):
        """
        在嵌套结构调用后
        :return:
        """
        self.__order = self.__number_list.pop()
        if not self.__invoke_interface:
            self.__order -= 1

    @staticmethod
    def __clear_context_with_res_and_req(context: dict):
        """
        清理context中的:
        __res_data__
        __res_header__
        __req_data__
        __req_header__
        :return:
        """
        if context.get("__res_data__") is not None:
            context.pop("__res_data__")
        if context.get("__res_header__") is not None:
            context.pop("__res_header__")
        if context.get("__req_data__") is not None:
            context.pop("__req_data__")
        if context.get("__req_header__") is not None:
            context.pop("__req_header__")

    @staticmethod
    def __get_specified_type_var(value, var_type):
        if var_type == "auto":
            if ParamType.is_int(value):
                var_type = "int"
            elif ParamType.is_float(value):
                var_type = "float"
            elif ParamType.is_bool(value):
                var_type = "bool"
            else:
                var_type = "str"
        if var_type == "str":
            value = str(value)
        elif var_type == "int":
            if not ParamType.is_int(str(value)):
                raise Exception("value值”{}”不是int类型".format(str(value)))
            value = ParamType.to_int(value)
        elif var_type == "float":
            if not ParamType.is_float(str(value)) and not ParamType.is_int(str(value)):
                raise Exception("value值”{}”不是float类型".format(str(value)))
            value = ParamType.to_float(value)
        elif var_type == "bool":
            value = str(value)
            if not ParamType.is_bool(str(value)):
                raise Exception("value值”{}”不是bool类型".format(str(value)))
            value = ParamType.to_bool(value)
        return value
