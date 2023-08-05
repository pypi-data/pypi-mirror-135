# -*- encoding=utf-8 *-*
"""
    author: Li Junxian
    function: frame config class
"""
import configparser
import os
import sys
import puppy

from ..utils.utils import Utils


class ConfigLoader(object):
    """
    项目的配置加载器
    """

    def __init__(self, config_file=None):
        # 用来存储全局变量得字典
        self.__global = dict()
        # 取到项目根目录
        self.__base_path = ConfigLoader.get_base_path()
        # puppy项目目录
        self.__puppy_path = puppy.__path__[0]
        if config_file:
            if os.path.isdir(config_file):
                raise Exception("配置文件是一个目录")
            if not os.path.exists(config_file):
                raise Exception("配置文件不存在")
            self.__config_file = config_file
        else:
            # 配置文件路径
            self.__config_file = "{}/file/conf/config.cfg".format(self.__base_path)
            if not os.path.exists(self.__config_file):
                self.__config_file = None
        # 默认配置
        self.__default_config = {
            "cases_path": os.path.join(self.__base_path, 'test_case'),
            "test_data_path": os.path.join(self.__base_path, 'test_data'),
            "flow_path": os.path.join(self.__base_path, 'flow'),
            "report_path": os.path.join(self.__base_path, "report"),
            "api_file_path": os.path.join(self.__base_path, "interface"),
            "jar_file_path": os.path.join(self.__base_path, "file/jar"),
            "js_file_path": os.path.join(self.__base_path, "file/js"),
            "file_path": os.path.join(self.__base_path, "file"),
            "inner_function_file": os.path.join(self.__puppy_path, "core", "function", "express", "function.py"),
            "outer_function_file": os.path.join(self.__base_path, "file/func.py"),
            "package_for_selenium": os.path.join(self.__base_path, "seleniums"),
            "browser": "Chrome",
            "driver": "None",
            "base_path": self.__base_path,
            "project_path": self.__base_path,
            "puppy_path": self.__puppy_path,
            "format_str_length": "-1",
            "report_name": "API自动化测试报告",
            "debug": "false",
            "cases": "test*.py",
            "http_connection_timeout": "50",
            "http_read_timeout": "50",
            "tcp_timeout": "60",
            "max_number_non_select_sql": "10",
            "resource_thread_sleep_time": "1",
            "progress_thread_sleep_time": "1",
            "action_case": "None",
            "db_keep_connection_time": "30",
            "testing": "false",
            "single_testing": "true",
            "the_global_inspection": "false",
            "the_global_inspection_type": "auto",
            "beautify": "true"
        }
        # 加载默认配置
        self.__conf = configparser.ConfigParser(self.__default_config)
        # 当存在配置文件时读取配置
        if self.__config_file:
            self.__conf.read(self.__config_file, encoding='utf-8')
        # 变量类型的配置存储
        self.__var_conf = {}

    @staticmethod
    def get_base_path():
        path = sys.path[0]
        if path.endswith("test_case"):
            return os.path.dirname(path)
        return path

    def __getattr__(self, name):
        """
        获得配置
        :param name:
        :return:
        """
        if name not in self.__global.keys():
            try:
                value = self.__conf.get("DEFAULT", name)
            except Exception:
                raise Exception("配置不存在：{}".format(name))
            else:
                from ..express.express import Express
                real_value = Express.calculate_str(value, {})
                self.__global[name] = real_value
        return str(self.__global[name])

    def __getitem__(self, item):
        """
        获得配置
        :param item:
        :return:
        """
        return self.__getattr__(item)

    def get_config(self, name, _type=str):
        """
        得到配置项，返回_type指定类型
        :param _type:
        :param name:
        :return: 如果配置不存在则返回None
        """
        cfg = self.__getattr__(name)
        if type(cfg) is not _type:
            if _type is bool:
                if cfg in ["True", "1", "true"]:
                    return True
                elif cfg in ["False", "0", "false"]:
                    return False
                else:
                    raise BaseException(" {} 配置项配置不正确，只能是True或False，不能是 {}".format(name, cfg))
            elif _type is int:
                if Utils.is_number(cfg):
                    return int(cfg)
                else:
                    raise BaseException(" {} 配置项不正确，只能是数字，不能是 {}".format(name, cfg))
        return self.__getattr__(name)

    def have_config(self, name):
        """
        判断是否存在配置
        :param name:
        :return:
        """
        try:
            self.__getattr__(name)
            return True
        except:
            return False

    def get_var(self, name):
        """
        得到变量值
        :param name:
        :return: 如果变量不存在返回错误标志
        """
        if name not in self.__global.keys():
            try:
                value = self.__conf.get("DEFAULT", name)
                from ..express.express import Express
                real_value = Express.calculate_str(value, {})
                self.__global[name] = real_value
            except Exception:
                return Utils.ERROR
        return self.__global[name]

    def set_config(self, name, value):
        """
        设置配置项，该配置项不会被写入文件。
        :param name:
        :param value:
        :return:
        """
        self.__global[name] = value

    def all_cases(self):
        self.set_config("cases", "test*.py")

    def start_test(self):
        print("自动化脚本测试开始！")
        self.set_config("format_str_length", -1)
        self.set_config("testing", True)
        self.set_config("single_testing", False)
        self.set_config("debug", False)
        self.set_config("the_global_inspection", True)

    def end_test(self):
        print("自动化脚本测试结束！")
        self.set_config("testing", False)

    def test(self, case):
        self.set_config("action_case", case)

    @property
    def report_name(self):
        return self.get_config("report_name")

    @property
    def cases(self):
        cases = self.get_config("cases")
        cases_list = cases.split("|")
        return cases_list


config = ConfigLoader()
