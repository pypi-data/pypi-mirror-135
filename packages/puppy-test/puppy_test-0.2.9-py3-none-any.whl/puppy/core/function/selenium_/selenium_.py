# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: selenium
"""
import importlib
import importlib.util
import os.path
from requests import Session
from ...function.cfg.config import config
from ...function.cookies.cookie import CookiesUtils
from ...function.func.func import Function


class Selenium_(object):
    __module_dict = dict()

    def __init__(self, module, function, browser=None, driver_path=None):
        """
        调用selenium函数
        :param module_name: 函数所在模块
        :param function_name: 函数名称
        :param browser: 可选项 浏览器
        :param driver: 可选项 driver路径
        """
        self.__module = module
        self.__function = function
        self.__browser = config.get_config("browser")
        if browser is not None:
            self.__browser = browser
        self.__driver_path = config.get_config("driver")
        if driver_path is not None:
            self.__driver_path = driver_path
        if self.__driver_path == "None":
            self.__driver_path = None

    @classmethod
    def is_exists_the_module(cls, module):
        """
        判断该module是否存在
        :param module:
        :return:
        """
        module_path = Selenium_.get_module_path(module)
        if os.path.exists(module_path):
            return True
        return False

    @classmethod
    def is_exists_the_func(cls, module, func):
        """
        判断指定module下存在指定func吗？
        :param module:
        :param func:
        :return:
        """
        if not Selenium_.is_exists_the_module(module):
            return False
        cls.__get_functions(module)
        return cls.__module_dict.get(module).has(func)

    @classmethod
    def get_module_path(cls, module):
        """
        取得module的路径
        :param module:
        :return:
        """
        package_path = config.get_config("package_for_selenium")
        return os.path.join(package_path, module + ".py")

    @classmethod
    def __get_functions(cls, module):
        """
        获取模块和函数
        :return:
        """
        if not Selenium_.is_exists_the_module(module):
            raise Exception("不存在名为 {} 的selenium模块".format(module))
        module_path = Selenium_.get_module_path(module)
        cls.__module_dict[module] = Function(module_path)

    def make_driver(self, session: Session):
        """
        取到执行driver,并传入session，当调用get时合并cookie
        :return:
        """
        if importlib.util.find_spec("selenium") is None:
            raise Exception("如需使用selenium，请安装selenium==3.141.0!")
        webdriver = importlib.import_module("selenium.webdriver")
        if "Chrome" == self.__browser:
            # 使用chrome浏览器
            if self.__driver_path:
                driver = webdriver.Chrome(self.__driver_path, keep_alive=True)
            else:
                driver = webdriver.Chrome(keep_alive=True)
        elif "Firefox" == self.__browser:
            # 使用火狐浏览器
            if self.__driver_path:
                driver = webdriver.Firefox(executable_path=self.__driver_path, keep_alive=True)
            else:
                driver = webdriver.Firefox(keep_alive=True)
        elif "Edge" == self.__browser:
            # 使用edge
            if self.__driver_path:
                driver = webdriver.Edge(executable_path=self.__driver_path, capabilities={}, keep_alive=True)
            else:
                driver = webdriver.Edge(capabilities={}, keep_alive=True)
        elif "Ie" == self.__browser:
            # 使用ie浏览器
            if self.__driver_path:
                driver = webdriver.Ie(executable_path=self.__driver_path)
            else:
                driver = webdriver.Ie()
        else:
            raise Exception("还不支持 {} 浏览器！".format(self.__browser))
        self.__add_method(driver, session)
        return driver

    def execute(self, driver, **kwargs):
        """
        执行本次selenium的调用
        :return:
        """
        # 根据函数名和模块名取到要执行的函数
        module: Function = Selenium_.__module_dict.get(self.__module)
        # 判断module是否存在，不存在则进入读取
        if module is None:
            self.__get_functions(self.__module)
            module = Selenium_.__module_dict.get(self.__module)
        # 取到函数
        if not module.has(self.__function):
            raise Exception("模块 {} 中没有函数 {}".format(self.__module, self.__function))
        func = module.fuc(self.__function)
        # 调用函数
        kwargs["driver"] = driver
        return func(**kwargs)

    def __add_method(self, driver, session: Session):
        """
        增加一些函数
        :param driver:
        :return:
        """
        def sync_cookies():
            """
            同步cookies
            """
            CookiesUtils.merge_requests_to_selenium(session, driver)

        setattr(driver, "sync_cookies", sync_cookies)