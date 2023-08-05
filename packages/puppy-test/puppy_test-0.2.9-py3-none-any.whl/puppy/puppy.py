import re
import subprocess
import zipfile
import puppy as _puppy
import shutil
import os
import unittest
import ctypes, sys
from .core.function.string.string_eplace_by_domains import StringReplaceByDomains
from .core.function.utils.params_proc import TransTextToXml

# 取到命令
params = sys.argv[1:]
command = " ".join(params)
# 取到当前项目目录
cwd = os.path.join(os.getcwd())
# 取到puppy的static目录
puppy_path = _puppy.__path__[0]
static_path = os.path.join(puppy_path, "static")
# 取到unittest的目录
unittest_path = unittest.__path__[0]

# 删除意外生成的文件
del_file_name = os.path.join(cwd, "file")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def exec_by_admin(file):
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, file, None, 1)
    else:
        raise Exception("python版本不受支持!")


def move_unittest_main():
    import unittest
    # 取到puppy的static目录
    puppy_path = _puppy.__path__[0]
    static_path = os.path.join(puppy_path, "static")
    # 取到unittest的目录
    unittest_path = unittest.__path__[0]
    # 替换默认的main.py
    # 先备份
    tmp_file = os.path.join(unittest_path, "tmp.txt")
    try:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
        with open(tmp_file, mode="w") as f:
            pass
    except:
        # 无权限，调用管理员模式
        exec_by_admin(os.path.join(static_path, "move_main.py"))
    else:
        # 有权限
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
        src_main_file = os.path.join(static_path, "main.py")
        main_file = os.path.join(unittest_path, "main.py")
        new_main_file = os.path.join(unittest_path, "main.py.backup")
        if os.path.exists(new_main_file):
            os.remove(new_main_file)
        if os.path.exists(main_file):
            shutil.copy(main_file, new_main_file)
            os.remove(main_file)
        shutil.copy(src_main_file, main_file)
        print("已完成main.py文件替换")


def __unzip(zip_file, dst="."):
    '''
    '''
    if dst == ".":
        dst = os.path.dirname(zip_file)
    with zipfile.ZipFile(file=zip_file, mode='r') as zf:
        for old_name in zf.namelist():
            # 由于源码遇到中文是cp437方式，所以解码成gbk，windows即可正常
            new_name = old_name.encode('cp437').decode('gbk')
            new_path = os.path.join(dst, new_name)
            if old_name.endswith("/"):
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
            else:
                if not os.path.exists(os.path.dirname(new_path)):
                    os.makedirs(os.path.dirname(new_path))
                with open(file=new_path, mode='wb') as f:
                    f.write(zf.read(old_name))


def __install_puppy_plugin():
    """
    安装插件
    :return:
    """
    app_data_path = os.environ["APPDATA"]
    jet_brains_path = os.path.join(app_data_path, "jetBrains")
    start_of_available_version = 20201
    end_of_available_version = 20211
    # 找到pycharm目录
    dir_list = list()
    for root, dirs, files in os.walk(jet_brains_path):
        for dir in dirs:
            if "PyCharm" in dir:
                # 取得版本号
                version = dir[7:]
                # 删除.
                int_type_of_version = _puppy.to_int(version)
                if start_of_available_version <= int_type_of_version <= end_of_available_version:
                    # 说明是受支持的pycharm
                    # 替换文件
                    pycharm_path = os.path.join(root, dir)
                    dir_list.append(pycharm_path)
    # 找到puppy插件安装包
    puppy_plugin_path = None
    puppy_plugin_name = None
    for root, dirs, files in os.walk(cwd):
        for file in files:
            if "PuppyPlugin-" in file:
                puppy_plugin_path = os.path.join(root, file)
                puppy_plugin_name, _ = os.path.splitext(file)
        break
    flag = None
    # 先删除已存在的PuppyPlugin
    for pycharm_path in dir_list:
        puppy_plugin_path_in_pycharm = os.path.join(pycharm_path, "plugins", "PuppyPlugin")
        if os.path.exists(puppy_plugin_path_in_pycharm):
            # 判断其版本是否一致
            if os.path.exists(os.path.join(puppy_plugin_path_in_pycharm, "lib", "{}.jar".format(puppy_plugin_name))):
                continue
            shutil.rmtree(puppy_plugin_path_in_pycharm)
        # 替换新的插件
        flag = True
        __unzip(puppy_plugin_path, os.path.join(pycharm_path, "plugins"))
    # 重启pycharm
    if flag:
        print("最后：请手动重启pycharm完成插件安装！")
    # 删除临时文件
    os.remove(puppy_plugin_path)


def init(_type):
    if _type == "auto":
        exclude_file = "unit"
    else:
        exclude_file = "auto"
    global params, command, cwd, puppy_path, static_path, unittest_path
    # 判断是否存在file文件夹或runner.py
    print("注意：您正在执行puppy的初始化命令，此命令会执行以下操作：")
    print("1、创建interface文件夹，并生成一个示例接口XML")
    print("2、创建flow文件夹，并生成一个示例流程XML")
    print("3、创建file/conf文件夹，并生成一个默认配置")
    print("4、创建file/xsd文件夹，并生成接口、流程、案例XML的语法约束文件")
    print("5、创建test_data文件夹，并生成一个示例案例XML")
    print("6、创建test_case模块，并生成一个示例案例XML对应的执行py文件")
    print("7、创建git版本控制忽略文件")
    print("8、创建puppy框架的自述文件")
    print("9、创建runner.py用于案例执行")
    print("10、替换Python单元测试框架UnitTest的main.py用于支持单个案例执行")
    print("11、安装pycharm的puppy插件")
    _i = input("确认执行以上操作，请输入y:")
    if _i not in ['y', 'Y']:
        print("终止操作！")
        exit(0)
    file_path = os.path.join(cwd, "file")
    runner_path = os.path.join(cwd, "runner.py")
    if os.path.exists(file_path) or os.path.exists(runner_path):
        print("")
        _i = input("注意：当前目录不是干净的！\n继续操作将会直接覆盖原有文件!\n建议使用puppy update进行配置升级!\n如需继续请输入y:")
        if _i not in ['y', 'Y']:
            print("终止操作！")
            exit(0)
    # 将static目录里的文件拷贝到当前项目
    files = list()
    for _root, _dirs, _files in os.walk(static_path):
        for _f in _files:
            files.append(os.path.join(_root, _f).replace(static_path + "\\", ""))
    for _f in files:
        dst = os.path.join(cwd, _f)
        # 包含main.py文件将不会被拷贝
        if exclude_file in _f:
            continue
        if "main.py" in _f:
            continue
        if "uncopy" in _f:
            continue
        if os.path.exists(dst):
            os.remove(dst)
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        src = os.path.join(static_path, _f)
        shutil.copy(src, dst)
    # 解压文件
    auto_zip = os.path.join(cwd, "{}.zip".format(_type))
    __unzip(auto_zip)
    os.remove(auto_zip)
    # 移动main.py文件
    move_unittest_main()
    print("已完成操作！")
    # 安装插件
    __install_puppy_plugin()


def update():
    # 从runner.py取得版本
    number_re = re.compile("\d+\.\d+\.\d+")
    runner_path = os.path.join(cwd, "runner.py")
    now_version = "0.0.0"
    if not os.path.exists(runner_path):
        print("未找到自动化测试关键性文件，请使用puppya init命令进行初始化！")
        return -1
    with open(runner_path, "r", encoding="utf-8") as file:
        for line in file.readlines():
            if "__version__" in line:
                number = number_re.findall(line)
                if len(number) == 0:
                    print("版本信息已被删除，无法继续执行升级！")
                    return -1
                now_version = number[0]
                break
    if _puppy.to_int(now_version) > _puppy.to_int(_puppy.get_version()):
        print("请先使用puppy upgrade升级puppy_test框架，再执行puppy update命令，如果已经是最新的puppy_test框架，说明代码的版本信息错误")
        return -1
    _i = input("以下操作将涉及到原文件的删除、修改，请勿终止此命令，否则将导致不可恢复的错误！！！\n建议提前开启Git，以恢复文件\n继续操作请输入y:")
    if _i not in ['y', 'Y']:
        print("终止操作！")
        return 0
    # 移动main.py文件
    move_unittest_main()
    print("当前脚本的版本是:{}".format(now_version))
    foot_update(now_version)
    # 移动文件
    # 文件检查列表
    check_file_list = [os.path.join("file", "conf", "config.cfg"),
                       os.path.join("file", "xsd", "flow.xsd"),
                       os.path.join("file", "xsd", "interface.xsd"),
                       os.path.join("file", "xsd", "scene.xsd"),
                       os.path.join("file", "func.py"),
                       "runner.py"]
    # 检查关键性文件是否存在
    for _f in check_file_list:
        now_file = os.path.join(cwd, _f)
        static_file = os.path.join(static_path, _f)
        if not os.path.exists(now_file):
            now_file_path = os.path.dirname(now_file)
            if not os.path.exists(now_file_path):
                os.makedirs(now_file_path)
            shutil.copy(static_file, now_file)
    # 替换xsd文件,runner文件
    replace_file_list = [os.path.join("file", "xsd", "flow.xsd"),
                         os.path.join("file", "xsd", "interface.xsd"),
                         os.path.join("file", "xsd", "scene.xsd"),
                         "runner.py"]
    for _f in replace_file_list:
        static_file = os.path.join(static_path, _f)
        new_file = os.path.join(cwd, _f)
        new_file_path = os.path.dirname(new_file)
        if not os.path.exists(new_file_path):
            os.makedirs(new_file_path)
        if os.path.exists(new_file):
            os.remove(new_file)
        shutil.copy(static_file, new_file)
    # 替换puppy插件
    puppy_plugin_path = None
    for root, dirs, files in os.walk(os.path.join(static_path)):
        for file in files:
            if "PuppyPlugin" in file:
                puppy_plugin_path = os.path.join(root, file)
                break
        if puppy_plugin_path:
            break
    if puppy_plugin_path:
        shutil.copy(puppy_plugin_path, cwd)
    print("已完成操作！")
    # 安装插件
    __install_puppy_plugin()
    return 0


def upgrade():
    server_version = _puppy.get_server_version()
    if server_version is None:
        print("服务器不通，请确认是否位于内网！")
        return -1
    if _puppy.to_int(server_version) <= _puppy.to_int(_puppy.get_version()):
        print("没有可供更新的puppy_test框架！")
        return -1
    cmd_list = ["start", "cmd.exe", "/k", "python", '"{}"'.format(os.path.join(static_path, "upgrade_main.py"))]
    cmd = " ".join(cmd_list)
    subprocess.Popen(cmd, shell=True)
    print("如果升级成功请再次执行puppy update继续更新当前工程版本！")


def clean():
    """
    清理工程
    :return:
    """
    # 先遍历test_case文件下的py文件名称，判断test_data内是否存在，如果存在则不操作，不存在则删除
    _i = input("以下操作将涉及到原文件的删除!\n继续操作请输入y:")
    if _i not in ['y', 'Y']:
        print("终止操作！")
        return 0
    path = os.path.join(cwd, "test_case")
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                name, _ = os.path.splitext(file)
                xml_name = os.path.join(cwd, "test_data", "{}.xml".format(name))
                if not os.path.exists(xml_name):
                    os.remove(os.path.join(root, file))
                    print("已移除无效PY文件：{}".format(file))


def generate():
    """
    生成案例
    :return:
    """
    print("敬请期待!")


def other(is_help=False):
    server_version = _puppy.get_server_version()
    now_version = None
    runner_path = os.path.join(cwd, "runner.py")
    number_re = re.compile("\d+\.\d+\.\d+")
    if os.path.exists(runner_path):
        with open(runner_path, "r", encoding="utf-8") as file:
            for line in file.readlines():
                if "__version__" in line:
                    number = number_re.findall(line)
                    if len(number) == 0:
                        break
                    now_version = number[0]
                    break
    desc = "        当前puppy-test框架版本为：{}\n".format(_puppy.get_version())
    if now_version is not None and _puppy.to_int(now_version) < _puppy.to_int(_puppy.get_version()):
        desc += "        当前工程的版本与框架版本不一致，请使用puppy update命令更新当前工程版本！\n"
    if server_version is not None and _puppy.to_int(server_version) > _puppy.to_int(_puppy.get_version()):
        desc += "        服务器有新的框架版本，请使用puppy upgrade命令升级！服务器的版本为：{}\n".format(server_version)
    if is_help:
        print("帮助：")
    else:
        print("命令输入错误！")
    print('''{}
        1、puppy init：    初始化工程
        2、puppy update：   更新当前工程版本
        3、puppy upgrade：  升级puppy-test框架（仅内网可用）
        4、puppy clean：  清理当前工程无用的文件（如test_case下未使用的py)
        5、puppy get-interface-from -f swagger txt文件：      将swagger txt文件转为框架可用的xml接口文件
        6、puppy generate-test-case -i 接口文件 -f 字段名 -r 构建规则：  自动生成测试案例（敬请期待!）
        7、puppy log：    展示puppy-test框架更新日志'''.format(desc))


def get_interface_from_swagger_txt(file_name):
    global cwd
    if not os.path.exists(file_name):
        file_path = os.path.join(cwd, file_name)
    else:
        file_path = file_name
    if not os.path.exists(file_path):
        print("指定的swagger txt文件不存在！")
        exit(-1)
    TransTextToXml(api_file_name=file_path).write_file()
    print("生成成功！")

def log():
    print('''更新日志：
    
    v0.2.8   2021年1月17日
    1、新增了swagger txt文档转接口xml的功能 
    ''')

def foot_update(now_version):
    if now_version == "0.0.0":
        # 从0开始升级
        print("脚本版本更新：0.0.0->0.0.1")
        now_version = "0.0.1"
        # 删除core文件夹
        core_path = os.path.join(cwd, "core")
        if os.path.exists(core_path):
            shutil.rmtree(core_path)
        # 删除plugins文件夹
        plugins_path = os.path.join(cwd, "plugins")
        if os.path.exists(plugins_path):
            shutil.rmtree(plugins_path)
        # 修改test_case文件夹下的内容
        test_case = os.path.join(cwd, "test_case")
        if os.path.exists(test_case):
            for root, dirs, files in os.walk(test_case):
                for file in files:
                    if not file.endswith(".py"):
                        continue
                    file_name = os.path.join(root, file)
                    with open(file_name, "r+", encoding="utf-8") as f:
                        lines = f.readlines()
                        content = "".join(lines)
                        if "APIProcessor" not in content:
                            continue
                        content = content.replace("core", "puppy.core")
                        content = content.replace("import unittest", "import unittest, runner")
                        f.truncate()
                        f.seek(0)
                        f.write(content)
        # 修改fun
        fun_path = os.path.join(cwd, "file", "func.py")
        if os.path.exists(fun_path):
            with open(fun_path, "r+", encoding="utf-8") as f:
                lines = f.readlines()
                content = "".join(lines)
                content = content.replace("from core", "from puppy.core")
                f.seek(0)
                f.write(content)
    if now_version == "0.0.1":
        print("脚本版本更新：0.0.1->0.0.2")
        now_version = "0.0.2"
    if now_version == "0.0.2":
        print("脚本版本更新：0.0.2->0.0.3")
        now_version = "0.0.3"
    if now_version == "0.0.3":
        print("脚本版本更新：0.0.3->0.0.4")
        now_version = "0.0.4"
    if now_version == "0.0.4":
        print("脚本版本更新：0.0.4->0.0.5")
        now_version = "0.0.5"
    if now_version == "0.0.5":
        print("脚本版本更新：0.0.5->0.0.6")
        now_version = "0.0.6"
        # 修改test_case文件夹下的内容
        temp_pattern_1 = re.compile(r">\s*\[\s*]\s*</expect>")
        temp_pattern_2 = re.compile(r">\s*\${\s*\[\s*]\s*}\s*</expect>")
        rep1 = ">\n                    [[]]\n                    </expect>"
        rep2 = ">\n                    ${[[]]}\n                    </expect>"

        def rep(string):
            string = temp_pattern_1.sub(rep1, string)
            string = string.replace("|[]", "|[[]]")
            string = string.replace("|${[]}", "|${[[]]}")
            return temp_pattern_2.sub(rep2, string)

        test_case = os.path.join(cwd, "test_data")
        if os.path.exists(test_case):
            for root, dirs, files in os.walk(test_case):
                for file in files:
                    if not file.endswith(".xml"):
                        continue
                    file_name = os.path.join(root, file)
                    with open(file_name, "r+", encoding="utf-8") as f:
                        lines = f.readlines()
                        content = "".join(lines)
                        if "scene" not in content:
                            continue
                        srb = StringReplaceByDomains(["<expect", "</expect>"], 'type="sql"')
                        content = srb.replace(content, rep)
                        f.truncate()
                        f.seek(0)
                        f.write(content)
    if now_version == "0.0.6":
        print("脚本版本更新：0.0.6->0.0.7")
        now_version = "0.0.7"
    if now_version == "0.0.7":
        print("脚本版本更新：0.0.7->0.0.8")
        now_version = "0.0.8"
    if now_version == "0.0.8":
        print("脚本版本更新：0.0.8->0.0.9")
        now_version = "0.0.9"
    if now_version == "0.0.9":
        print("脚本版本更新：0.0.9->0.1.0")
        now_version = "0.1.0"
    if now_version == "0.1.0":
        print("脚本版本更新：0.1.0->0.1.1")
        now_version = "0.1.1"
    if now_version == "0.1.1":
        print("脚本版本更新：0.1.1->0.1.2")
        now_version = "0.1.2"
    if now_version == "0.1.2":
        print("脚本版本更新：0.1.2->0.1.3")
        now_version = "0.1.3"
    if now_version == "0.1.3":
        print("脚本版本更新：0.1.3->0.1.4")
        now_version = "0.1.4"
    if now_version == "0.1.4":
        print("脚本版本更新：0.1.4->0.1.5")
        now_version = "0.1.5"
    if now_version == "0.1.5":
        print("脚本版本更新：0.1.5->0.1.6")
        now_version = "0.1.6"
    if now_version == "0.1.6":
        print("脚本版本更新：0.1.6->0.1.7")
        now_version = "0.1.7"
    if now_version == "0.1.7":
        print("脚本版本更新：0.1.7->0.1.8")
        now_version = "0.1.8"
    if now_version == "0.1.8":
        print("脚本版本更新：0.1.8->0.1.9")
        now_version = "0.1.9"
    if now_version == "0.1.9":
        print("脚本版本更新：0.1.9->0.2.0")
        now_version = "0.2.0"
    if now_version == "0.2.0":
        print("脚本版本更新：0.2.0->0.2.1")
        now_version = "0.2.1"
    if now_version == "0.2.1":
        print("脚本版本更新：0.2.1->0.2.2")
        now_version = "0.2.2"
    if now_version == "0.2.2":
        print("脚本版本更新：0.2.2->0.2.3")
        now_version = "0.2.3"
    if now_version == "0.2.3":
        print("脚本版本更新：0.2.3->0.2.4")
        now_version = "0.2.4"
    if now_version == "0.2.4":
        print("脚本版本更新：0.2.4->0.2.5")
        now_version = "0.2.5"
    if now_version == "0.2.5":
        print("脚本版本更新：0.2.5->0.2.6")
        now_version = "0.2.6"
    if now_version == "0.2.6":
        print("脚本版本更新：0.2.6->0.2.7")
        now_version = "0.2.7"
    if now_version == "0.2.7":
        print("脚本版本更新：0.2.7->0.2.8")
        now_version = "0.2.8"
    if now_version == "0.2.8":
        #将translnterfaceTextToXml.py复制到当前项目的interface目录下
        src_file=os.path.join(static_path,"uncopy","transInterfaceTextToXml.py")
        new_file=os.path.join(cwd,"interface","transInterfaceTextToXml.py")
        new_path=os.path.dirname(new_file)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        if os.path.exists(new_file):
            os.remove(new_file)
        shutil.copy(src_file, new_file)
        print("脚本版本更新：0.2.8->0.2.9")
        now_version = "0.2.9"


def main():
    global command
    command = command.replace(" ", "")
    if command == "init-tunit" or command == "init":
        init("unit")
    elif command == "init-tauto":
        init("auto")
    elif command == "update":
        update()
    elif command == "upgrade":
        upgrade()
    elif command == "clean":
        clean()
    elif "generate-test-case" in command:
        generate()
    elif "get-interface-from-f" in command:
        file_name = command[20:]
        get_interface_from_swagger_txt(file_name)
    elif command == "help":
        other(True)
    elif command=="log":
        log()
    else:
        other()


