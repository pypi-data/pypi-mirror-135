# -*- encoding=utf-8 *-*
"""
    author: Li Junxian
    function: beautify json
"""
import re
from ..parse.json_parse import JsonParse
from ..utils.utils import Utils


class BeautifyJson(object):
    __blank_re = re.compile(r"\s")
    __blank = Utils.BLANK_CHAR
    __single = 2

    def __init__(self, json: str):
        """
        待美化的json字符串
        :param json:
        """
        self.__json = json
        if not JsonParse.is_correct_json(json):
            raise Exception("{}不是正确的json字符串".format(json))
        self.__beautified_json = ""

    def beautify(self):
        """
        获得美化后的json字符串
        :return:
        """
        # 空白字符
        # 空白字符所有数量
        number_of_blank = 3
        # 单级空白字符数量
        json_list = list(self.__json)
        double_quotation_marks = False
        backslash = False
        first = True
        last_letter = None
        for letter in json_list:
            if BeautifyJson.__blank_re.fullmatch(letter) and not double_quotation_marks:
                pass
            elif letter == "\\":
                backslash = not backslash
                self.__beautified_json += letter
            elif letter == '"' and not backslash:
                double_quotation_marks = not double_quotation_marks
                self.__beautified_json += '"'
            elif letter in ['{', '['] and not double_quotation_marks:
                if first:
                    self.__beautified_json += "{}{}\n".format(BeautifyJson.__blank * number_of_blank, letter)
                    first = False
                else:
                    self.__beautified_json += "{}\n".format(letter)
                number_of_blank += BeautifyJson.__single
                self.__beautified_json += BeautifyJson.__blank * number_of_blank
            elif letter == ':' and not double_quotation_marks:
                self.__beautified_json += ": "
            elif letter in [']', '}'] and not double_quotation_marks:
                number_of_blank -= BeautifyJson.__single
                if last_letter in ['[', '{']:
                    self.__beautified_json=self.__beautified_json.rstrip()
                    self.__beautified_json += "{}".format(letter)
                else:
                    self.__beautified_json += "\n{}{}".format(BeautifyJson.__blank * number_of_blank, letter)
            elif letter == ',' and not double_quotation_marks:
                self.__beautified_json += ",\n{}".format(BeautifyJson.__blank * number_of_blank)
            else:
                backslash = False
                self.__beautified_json += letter
            last_letter = letter
        return self.__beautified_json
