"""执行命令"""

import pexpect
import getpass
import time

import globals as gl
import config as cf
import utils as ut


password_prompt = 'password:'
password_prompt_zh = '密码：' # 系统的密码提示符



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



def replace_quotes(input_string):
    """替换字符串中的双引号至单引号"""

    in_single_quote = False
    in_double_quote = False
    escaped = False
    result = []

    for char in input_string:
        if escaped:
            # 上一个字符是转义符，当前字符不做处理
            result.append(char)
            escaped = False
        elif char == '\\':
            # 当前字符是转义符，标记并添加到结果
            result.append(char)
            escaped = True
        elif char == '"':
            if in_single_quote:
                # 在单引号内，视为普通字符
                result.append(char)
            elif in_double_quote:
                # 在双引号内，结束双引号区域
                result.append("'")
                in_double_quote = False
            else:
                # 不在引号内，替换为单引号
                result.append("'")
                in_double_quote = True
        elif char == "'":
            if in_double_quote:
                # 在双引号内，视为普通字符
                result.append(char)
            elif in_single_quote:
                # 在单引号内，结束单引号区域
                result.append(char)
                in_single_quote = False
            else:
                # 不在引号内，开始单引号区域
                result.append(char)
                in_single_quote = True
        else:
            result.append(char)

    return ''.join(result)



def execute_command(raw_command, need_confirm = True, print_result = True):
    """执行命令"""

    command = replace_quotes(raw_command)

    # 如果命令包含sudo，则需要确认
    if ('sudo' in command) or need_confirm:
        ut.print_spoker()
        confirm_state = ut.confirm("是否执行命令\"" + ut.set_color(command, cf.program_name_color) + "\" ?")
        if not confirm_state:
            raise ValueError("用户拒绝执行命令。")
    
    if print_result:
        ut.print_spoker(ut.set_color(cf.system_name, cf.system_name_color), cf.system_name)

    child = pexpect.spawn(f'/bin/bash -c "{command}"', encoding='utf-8', maxread=8192)

    try:
        pass_retry = False # 重置重试次数
        output = ""

        while True:
            i = child.expect([password_prompt, password_prompt_zh, '\[Y/n\]', '\[y/n\]', pexpect.EOF, \
                pexpect.TIMEOUT,'\n','=','#','%','\t','\b'], timeout=20)

            match i: 

                case 0 | 1: # 等待密码提示
                    if pass_retry:
                        password = getpass.getpass("密码错误，请再次尝试：")
                    else:
                        password = getpass.getpass("请输入管理员密码：")
                    pass_retry = True
                    child.sendline(password)

                case 2 | 3:
                    text = (child.before.strip() if child.before is not None else "") + "[Y/n]"
                    print(text, end='')
                    user_inputs = input()
                    child.sendline(user_inputs)
                    output += text + user_inputs + "\n"

                case 4:  # EOF，命令执行完成
                    if print_result:
                        print(child.before.strip(), end='')
                    return clean_backspaces(output + child.before.strip())

                case 5:  # 超时
                    raise TimeoutError("命令执行超时。")

                case _:
                    text = (child.before.strip() if child.before is not None else "")
                    match i:
                        case 6:
                            text += '\n'
                        case 7:
                            text += '='
                        case 8:
                            text += '#'
                        case 9:
                            text += '%'
                        case 10:
                            text += '\t'
                        case 11:
                            text += '\b'
                    output += text
                    if print_result:
                        print(text, end="")

    except pexpect.exceptions.EOF: # 子进程被异常终止
        raise EOFError("子程序被异常终止。") from None
    except Exception as e: # 发生异常
        raise Exception("发生异常"+str(e)) from e


