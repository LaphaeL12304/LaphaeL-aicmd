"""执行命令 - Execute the command"""

from ptyprocess import PtyProcessUnicode
import shlex
import getpass
import os

from . import globals as gl
from . import config as cf
from . import utils as ut

password_prompt = 'password:'
password_prompt_zh = '密码：'  # 系统的密码提示符 - password prompt of system


def clean_backspaces(input_string: str) -> str:
    """
    Remove backspace characters from a string.
    去除字符串中的删除符
    """

    result = []

    for char in input_string:
        if char == '\b':
            if result:
                result.pop()  # 删除前一个字符 - Remove the previous character
        else:
            result.append(char)  # 添加当前字符 - Add the current character

    return ''.join(result)


def execute_command(command: str, need_confirm: bool=True, print_result: bool=True) -> str:
    """
    Execute a shell command, optionally requiring confirmation and printing the result.
    执行一个shell命令，可选地需要确认并打印结果。

    :param command: The command to execute 要执行的命令
    :param need_confirm: Whether to require confirmation 是否需要确认
    :param print_result: Whether to print the result 是否打印结果
    :return: The cleaned result of the command execution 命令执行的清理后的结果
    """
    # 如果命令包含'sudo'或需要确认，则请求确认    
    # If the command contains 'sudo' or confirmation is needed, ask for confirmation
    if ('sudo' in command) or need_confirm:
        ut.print_spoker()
        confirm_state = ut.confirm("是否执行命令\"" + ut.set_color(command, cf.program_name_color) + "\" ?")
        if not confirm_state:
            raise ValueError("用户拒绝执行命令。")

    if print_result:
        ut.print_spoker(ut.set_color(cf.system_name, cf.system_name_color), cf.system_name)

   # 包装命令以通过bash执行
    # Wrap the command to be executed via bash
    wrapped_command = ['bash', '-c', command]
    process = PtyProcessUnicode.spawn(wrapped_command)  # 使用bash -c来执行命令 - Use bash -c to execute the command
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


def match_before(before: str, process: PtyProcessUnicode) -> bool:
    """
    Match the output content and interact accordingly.
    匹配输出中的内容并进行交互

    :param before: The output before the current point 当前点之前的输出
    :param process: The process object 进程对象
    :return: Whether a match was found 是否找到匹配
    """
    match_list = [password_prompt, password_prompt_zh, '[y/n]', '[Y/n]']
    for i in range(len(match_list)):
        if match_list[i] in before.strip():

            match i:
                case 0 | 1:
                    print('\r' + ' ' * os.get_terminal_size().columns + '\r', end='')
                    password = getpass.getpass(ut.set_color("请输入管理员密码：", cf.system_name_color))
                    process.write(password + "\n")

                case 2 | 3:
                    user_input = input(ut.set_color('[Y/n]', cf.system_name_color))
                    process.write(user_input + "\n")

                case _:
                    pass

            return True
    return False