"""
    author: Li Junxian
    function:is used to process function
"""
import importlib
import os
import re


class Function(object):
    """
    功能读取、调用、帮助信息输出
    """
    __function_name_re = re.compile(r"def\s+[a-zA-Z0-9_]+")

    def __init__(self, func_file):
        """
        func_file:功能py文件全路径
        """
        self.__model_name = None
        self.__help = None
        self.__help_info = {}
        self.__func = {}
        self.__names = []
        self.__func_file = func_file
        if not os.path.exists(func_file):
            raise Exception("{} 不存在".format(func_file))
        self.__get_functions_name()
        self.__split_model_name()
        self.__get_func()
        self.__get_help()

    def __get_functions_name(self):
        with open(self.__func_file, encoding="utf-8") as file:
            contents = file.readlines()
        # 使用正则提取方法名称
        for content in contents:
            result = self.__function_name_re.match(content)
            if not result:
                continue
            func_name = result.group().split(" ")[-1]
            if func_name.startswith("__"):
                continue
            self.__names.append(func_name)

    def __get_func(self):
        """
        取得func信息
        """
        func = importlib.import_module(self.__model_name)
        for name in self.__names:
            self.__func[name] = getattr(func, name)

    def __get_help(self):
        """
        获取help信息
        """
        for name in self.__names:
            doc = self.__func[name].__doc__
            doc = "" if doc is None else doc
            self.__help_info[name] = doc.strip()

    def __split_model_name(self):
        """
        获取到包名和模块名
        """
        # 取得根目录
        from ..cfg.config import config
        import puppy
        base_path = config.base_path
        # 取得puppy模块的目录
        puppy_path = os.path.dirname(config.get_config("puppy_path"))
        # 将文件名拆开
        model_name, suffix = os.path.splitext(self.__func_file)
        if base_path in model_name:
            model_name = model_name.replace(base_path, "")
        if puppy_path in model_name:
            model_name = model_name.replace(puppy_path, "")
        if model_name[0] in ["\\", "/"]:
            model_name = model_name[1:]
        # 遍历字符串
        new_model_name = ""
        for s in list(model_name):
            if s in ["/", "\\"]:
                new_model_name += "."
            else:
                new_model_name += s
        self.__model_name = new_model_name

    def help(self, number):
        """
        输出帮助信息
        """
        if self.__help:
            return self.__help
        msg = ""
        for name, info in self.__help_info.items():
            msg += "{}、{}:\n  {}\n".format(number, name, info)
            number += 1
        return msg, number

    def has(self, name):
        """
        判断是否有此方法
        """
        if name in self.__names:
            return True
        return False

    def fuc(self, name):
        """
        取得要调用的方法
        """
        if not self.has(name):
            raise Exception("此{}函数不存在!".format(name))
        return self.__func[name]
