#!/usr/bin/env python3

"""
This program is named 'aicmd_Linux', it allows chat AI to execute commands on the user's Linux system.
Copyright (C) 2024 LaphaeL
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pexpect
import getpass
import google.generativeai as genai
import time
import sys
import re
import os

# 声明路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
readme_for_AI_path = os.path.join(project_root, "data", "README_for_AI.txt")
custom_instruct_path = os.path.join(project_root, "data", "custom_instruct.txt")

# 配置API密钥
api_key = "Your-API-Key"
genai.configure(api_key=api_key)
# 初始化Gemini模型
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

#声明程序信息
program_name = "\033[35;1maicmd\033[0m"
ai_name = "\033[34;1mGemini\033[0m"

password_prompt = 'password:'
password_prompt_zh = '密码：' # 系统的密码提示符

print_history = ""

slow_print_enter = 0

pwd_path = ""
ls_home = ""
system_version = ""



def extract_command(text):
    """匹配被"///"包裹的文本"""
    pattern = r'///(.*?)///'
    match = re.search(pattern, text)  # 查找第一个匹配项
    return match.group(1) if match else ""  # 如果没有匹配项则返回空



def slow_print(text, delay=0.002, enter=True):
    """逐字打印文本，每个字之间延时 delay 秒"""
    global slow_print_enter
    for char in text:
        if char == "\n":
            if slow_print_enter >= 2: # 清除连续换行
                continue
            slow_print_enter += 1
            print("", flush=True) # 打印换行
        elif char not in ("*", "`"):  # 检查字符是否是要跳过的字符
            print(char, end='', flush=True)
            slow_print_enter = 0
            time.sleep(delay)
    if enter:
        print()  # 打印换行
    slow_print_enter = 0


def print_spoker(printer_name = program_name):
    """打印发言人"""
    global last_printer, print_history
    if printer_name != last_printer:
        slow_print(printer_name + ": ", enter=False)
        print_history += printer_name[7:-4] + ": "
    last_printer = printer_name



def interact_with_gemini(chat, ai_input):
    """与Gemini API进行对话，并利用流式传输逐字打印回答"""
    global print_history
    print_spoker(ai_name)
    response = chat.send_message(ai_input, stream=True)
    ai_text = ""
    for chunk in response:
        slow_print("\033[36;1m" + chunk.text + "\033[0m")
        ai_text += chunk.text
    print_history += "#省略AI的回答\n"
    return ai_text.strip()


def confirm(printstr = "是否同意?"):
    """打印[Y/n]确认界面"""
    global print_history
    print_spoker()
    slow_print(printstr, enter=False)
    t = "[Y/n]"
    result = input(t)
    print_history += printstr + t + result + "\n"
    return True if result.lower() == 'y' or (not result) else False # 如果输入y或无输入，则返回True


def read_file(file_path):
    """读取文件"""
    if not os.path.exists(file_path):
        return "///文件不存在"
    else:
        try:
            # 打开文件，指定相对路径
            with open(file_path, 'r', encoding='utf-8') as file:
                # 返回文件内容到字符串
                return file.read()
        except Exception as e:
            return f"///{str(e)}"

    

def execute_command(command_raw, need_confirm = True):
    """执行命令"""
    global print_history, pwd_path
    command = command_raw.replace('~', pwd_path) # 将'~'替换为当前目录
    # 如果命令包含sudo，则需要确认
    if ('sudo' in command) or need_confirm:
        confirm_state = confirm(f"是否执行命令 \033[35;1m\"{command}\"\033[0m ？")
        if not confirm_state:
            return "///用户拒绝执行命令。"
    
    child = pexpect.spawn(f'/bin/bash -c "{command}"', encoding='utf-8')
    try:
        passretry = False # 重置重试次数
        while True:
            i = child.expect([password_prompt, password_prompt_zh, pexpect.EOF, \
                pexpect.TIMEOUT], timeout=10)
            match i:  # 等待密码提示
                case 0 | 1:
                    if passretry:
                        t = "密码错误，请再次尝试："
                        password = getpass.getpass(t)
                        print_history += t + "\n"
                    else:
                        t = "请输入管理员密码："
                        password = getpass.getpass(t)
                        print_history += t + "\n"
                    passretry = True
                    child.sendline(password)
                case 2:  # EOF，命令执行完成
                    return child.before.strip()
                case 3:  # 超时
                    return "///命令执行超时。"

    except pexpect.exceptions.EOF: # 子进程被异常终止
        return "///子进程被异常终止。"
    except Exception as e: # 发生异常
        return f"///发生异常 - {str(e)}"


def match_instruction(instruction):
    """处理用户输入的指令"""
    global print_history

    if instruction.startswith('/cmd '):
        system_output = execute_command(instruction[5:], False) # 执行此命令命令
        if system_output.startswith('///'): # 命令执行异常
            print_spoker(program_name)
            slow_print(system_output[3:]) # 打印异常信息
            print_history += system_output[3:] + "\n"
        else:
            print_spoker(system_name)
            slow_print(system_output) # 打印命令执行结果
            print_history += system_output + "\n"
    else:
        print_spoker(program_name)
        match instruction: # 如果用户输入以'/'开头，则匹配用户输入
            case "/exit" | "/退出": # 退出程序
                slow_print("正在退出程序...")
                sys.exit(0)
            case "/help" | "/帮助" | "/": # 打印帮助文本
                print_spoker(program_name)
                t = "这是帮助文本，暂时没写"
                slow_print(t)
                print_history += t + "\n"
            case "/history" | "/历史": # 打印历史记录
                print_spoker(program_name)
                slow_print("以下是历史记录：\n" + print_history)
                print_history += "#省略历史记录打印\n"
            case "/clear" | "/清空": # 清空历史记录
                print_history = ""
                print_spoker(program_name)
                t = "历史记录已清空"
                slow_print(t)
                print_history += t + "\n"
            case _: # 其他情况
                print_spoker(program_name)
                t = "无效指令"
                slow_print(t)
                print_history += t + "\n"
    

def init():
    """初始化"""
    slow_print(program_name + ": 正在初始化...")

    # 初始化变量
    global slow_print_enter, last_printer, print_history
    global pwd_path, ls_home, system_version
    global system_name_raw, user_name_raw, system_name, user_name
    slow_print_enter = 0
    last_printer = ""
    print_history = ""

    slow_print("正在获取系统信息...")
    # 获取计算机信息
    pwd_path = execute_command("pwd", False)
    ls_home = execute_command("ls", False)
    result = execute_command("lsb_release -a", False)

    system_version = "System verison unkown"
    for line in result.split('\n'):
            if 'description:' in line.lower():
                # 获取干净的系统信息
                system_version = line.split(':')[1].strip()
                break
    system_name_raw = system_version.split()[0]
    user_name_raw = execute_command("whoami", False)
    system_name = "\033[33;1m" + system_name_raw + "\033[0m"
    user_name = "\033[32;1m" + user_name_raw + "\033[0m"


    slow_print("正在获取配置文件...")
    # 读取文件
    readme_for_AI = read_file(readme_for_AI_path)
    custom_instruct = read_file(custom_instruct_path)

    if readme_for_AI.startswith("///"):
        sys.exit("'README_for_AI.txt'读取错误：" + readme_for_AI[3:])
    elif not readme_for_AI:
        sys.exit("'README_for_AI.txt'为空")
    elif custom_instruct.startswith("///"):
        sys.exit("'custom_instruct.txt'读取错误：" + custom_instruct[3:])
    elif not custom_instruct:
        sys.exit("'custom_instruct.txt'为空")

    # 连接AI
    slow_print("正在尝试连接到\"" + ai_name + "\"...")
    init_prompt = readme_for_AI + \
        "\n以下是用户计算机信息:\n(" + \
        "\n系统版本: " + system_version+ \
        "\n用户名: " + user_name + \
        "\nhome目录下的文件: " + ls_home + \
        "\n)\n" + custom_instruct +\
        "\n如果你能理解以上要求，请回复\"准备就绪\"。"
    ai_output = interact_with_gemini(chat, init_prompt)
    if not ("准备就绪" in ai_output.lower() or "ready" in ai_output.lower()):
        sys.exit("连接失败或AI无法理解要求")
    print_spoker(program_name)
    slow_print("连接成功！\"" + ai_name[7:-4] + "\"已经理解程序要求")
    
    slow_print("\"" + program_name[7:-4] + "\"已准备就绪！\n")


def main():

    global print_history
    init()

    control_on_user = True # 控制权在用户
    while True:

        if control_on_user: # 控制权在用户
            print_spoker(user_name) # 打印用户信息
            user_input = input() # 接收用户输入
            print_history += user_input + "\n" # 记录用户输入
            # 处理用户输入
            if user_input.startswith('/'):
                match_instruction(user_input)
            elif user_input: # 如果输入不以'/'开头，且输入不为空，则发送给AI
                control_on_user = False # 控制权在AI

        else: #控制权在AI
            ai_output = interact_with_gemini(chat, print_history) # 与AI交互
            ai_output_command = extract_command(ai_output)
            print_history = "" # 清空历史记录

            if ai_output_command:
                system_output = execute_command(ai_output_command) # 执行AI输出的命令
                if system_output.startswith('///'): # 命令执行异常
                    print_spoker(program_name)
                    slow_print(system_output[3:]) # 打印异常信息
                    print_history += system_output[3:] + "\n"
                else:
                    print_spoker(system_name)
                    slow_print(system_output) # 打印命令执行结果
                    print_history += system_output + "\n"
            else:
                control_on_user = True


if __name__ == "__main__":
    main()
