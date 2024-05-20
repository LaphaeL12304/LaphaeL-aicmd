from ptyprocess import PtyProcessUnicode
import shlex
import getpass
import os

from . import globals as gl
from . import config as cf
from . import utils as ut

password_prompt = 'password:'
password_prompt_zh = '密码：'  # 系统的密码提示符


def clean_backspaces(input_string):
    """去除字符串中的删除符"""

    result = []

    for char in input_string:
        if char == '\b':
            if result:
                result.pop()  # 删除前一个字符
        else:
            result.append(char)  # 添加当前字符

    return ''.join(result)



def execute_command(command, need_confirm=True, print_result=True):
    # 如果命令包含sudo，则需要确认
    if ('sudo' in command) or need_confirm:
        ut.print_spoker()
        confirm_state = ut.confirm("是否执行命令\"" + ut.set_color(command, cf.program_name_color) + "\" ?")
        if not confirm_state:
            raise ValueError("用户拒绝执行命令。")

    if print_result:
        ut.print_spoker(ut.set_color(cf.system_name, cf.system_name_color), cf.system_name)

    # 包装命令以通过bash执行
    wrapped_command = ['bash', '-c', command]
    process = PtyProcessUnicode.spawn(wrapped_command)  # 使用bash -c来执行命令
    result = ""
    before = ""

    try:
        while True:
            output = process.read(1)
            if output == '':
                if process.eof():
                    break
            if print_result:
                print(output, end='', flush=True)
            result += output
            before += output
            matched = match_before(before, process)
            if matched:
                before = ""
    except EOFError:
        pass
    except Exception as e:
        print("发生错误:", e)

    process.terminate()
    process.wait()

    if print_result:
        t = ut.set_color("执行完毕", cf.system_name_color)
        result += t
        print(t.strip())

    return clean_backspaces(result.strip())



def match_before(before, process):
    """匹配输出中的内容并进行交互"""
    match_list = [password_prompt, password_prompt_zh, "[y/n]"]
    for prompt in match_list:
        if prompt.lower() in before:
            if prompt.lower() in (password_prompt, password_prompt_zh):
                print('\r' + ' ' * os.get_terminal_size().columns + '\r', end='')
                password = getpass.getpass(ut.set_color("请输入管理员密码：", cf.system_name_color))
                process.write(password + "\n")
            
            elif prompt.lower() in ("[y/n]"):
                user_input = input(ut.set_color("[Y/n]", cf.system_name_color))
                process.write(user_input + "\n")

            return True

    return False