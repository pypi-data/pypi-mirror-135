import ctypes
import sys
import puppy


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


if puppy.upgrade_puppy_test() == 0:
    print("已升级成功！请手动关闭此窗口！")
elif not is_admin():
    print("升级失败，尝试申请管理员权限进行升级！")
    exec_by_admin(__file__)
