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


import record_history
import _color_string
import _print_spoker as sp
import _user_confirm
import slow_print
import execute_cmd as cmd
import chat_gemini



# 声明路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
instruction_prompt_path = os.path.join(project_root, "data", "instruction_prompt.txt")
custom_instruct_path = os.path.join(project_root, "data", "custom_instruct.txt")



#声明程序信息
program_name = _color_string.Color_str("AIcmd", "purple", "bold")
ai_name = _color_string.Color_str("Gemini", "blue", "bold")


# 实例化
print_history = record_history.History()
current_command = cmd.Command(program_name.text)
print_sp = sp.print_spoker(program_name)

def spoke(name = program_name):
    print_sp(name)
    print_history.add(name.raw + ": ")

chat_ai = chat_gemini.chat_AI_gemini("Gemini", 'gemini-pro')
chat_ai.api = "Your-API-Key"
chat_ai.initialize()


# 声明变量
pwd_path = ""
ls_home = ""
system_version = ""



def extract_command(text):
    """匹配被"///"包裹的文本"""
    pattern = r'///(.*?)///'
    match = re.search(pattern, text)  # 查找第一个匹配项
    return match.group(1) if match else ""  # 如果没有匹配项则返回空



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



def match_instruction(instruction):
    """处理用户输入的指令"""

    if instruction.startswith('/cmd '):
        try:
            current_command.text = instruction[5:]
            system_output = current_command.execute(False) # 执行此命令命令
            spoke(system_name)
            slow_print.slow_print(system_output) # 打印命令执行结果
            print_history.add_line(system_output)
        except Exception as e:
            spoke()
            slow_print.slow_print(str(e)) # 打印异常信息
            print_history.add_line(str(e))
    
    else:
        spoke()
        match instruction: # 如果用户输入以'/'开头，则匹配用户输入
            case "/exit" | "/退出": # 退出程序
                slow_print.slow_print("正在退出程序...")
                sys.exit(0)
            case "/help" | "/帮助" | "/": # 打印帮助文本
                spoke()
                t = "这是帮助文本，暂时没写"
                slow_print.slow_print(t)
                print_history.add_line(t)
            case "/history" | "/历史": # 打印历史记录
                spoke()
                slow_print.slow_print("以下是历史记录：\n" + print_history.text)
                print_history.add_line("#省略历史记录打印")
            case "/clear" | "/清空": # 清空历史记录
                print_history.clear()
                spoke()
                slow_print.slow_print("历史记录已清空")
            case _: # 其他情况
                spoke()
                t = "无效指令"
                slow_print.slow_print(t)
                print_history.add_line(t)
    


def initialize():
    """初始化"""
    slow_print.slow_print(program_name.text + ": 正在初始化...")

    # 初始化变量
    global pwd_path, ls_home, system_version
    global system_name, user_name
    slow_print.slow_print_enter = 0
    last_printer = ""
    print_history.clear()

    slow_print.slow_print("正在获取系统信息...")
    # 获取计算机信息
    try:
        current_command.text = "pwd"
        pwd_path = current_command.execute(False)
        current_command.text = "ls"
        ls_home = current_command.execute(False)
        current_command.text = "whoami"
        user_name = _color_string.Color_str(current_command.execute(False), "green", "bold")
        current_command.text = "lsb_release -a"
        result = current_command.execute(False)
    except Exception as e:
        spoke()
        sys.exit("获取信息失败："+ str(e))

    print(pwd_path)
    print(ls_home)

    system_version = "System verison unkown"
    for line in result.split('\n'):
            if 'description:' in line.lower():
                # 获取干净的系统信息
                system_version = line.split(':')[1].strip()
                break
    system_name = _color_string.Color_str(system_version.split()[0], "yellow", "bold")
    


    slow_print.slow_print("正在获取配置文件...")
    # 读取文件
    instruction_prompt = read_file(instruction_prompt_path)
    custom_instruct = read_file(custom_instruct_path)

    if instruction_prompt.startswith("///"):
        sys.exit("'instruction_prompt.txt'读取错误：" + instruction_prompt[3:])
    elif not instruction_prompt:
        sys.exit("'instruction_prompt.txt'为空")
    elif custom_instruct.startswith("///"):
        sys.exit("'custom_instruct.txt'读取错误：" + custom_instruct[3:])
    elif not custom_instruct:
        sys.exit("'custom_instruct.txt'为空")


    # 连接AI
    slow_print.slow_print("正在尝试连接到\"" + ai_name.raw + "\"...")
    init_prompt = instruction_prompt + \
        "\n以下是用户计算机信息:\n(" + \
        "\n系统版本: " + system_version+ \
        "\n用户名: " + user_name.raw + \
        "\nhome目录下的文件: " + ls_home + \
        "\n)\n" + custom_instruct +\
        "\n如果你能理解以上要求，请回复\"准备就绪\"。"
    ai_output = chat_ai.interact(init_prompt, print_history, print_sp)
    # ai_output = interact_with_gemini(chat, init_prompt)
    if not ("准备就绪" in ai_output.lower() or "ready" in ai_output.lower()):
        sys.exit("连接失败或AI无法理解要求")

    

    spoke()
    slow_print.slow_print("连接成功！\"" + ai_name.raw + "\"已经理解程序要求")
    
    slow_print.slow_print("\"" + program_name.raw + "\"已准备就绪！\n")
    print_history.clear()



def main():

    initialize()

    control_on_user = True # 控制权在用户
    while True:

        if control_on_user: # 控制权在用户
            spoke(user_name) # 打印用户信息
            user_input = input() # 接收用户输入
            print_history.add_line(user_input)# 记录用户输入
            # 处理用户输入
            if user_input.startswith('/'):
                match_instruction(user_input)
            elif user_input: # 如果输入不以'/'开头，且输入不为空，则发送给AI
                control_on_user = False # 控制权在AI

        else: #控制权在AI
            # print(print_history.text) # 查看向AI发送的历史记录，仅调试用
            ai_output = chat_ai.interact(print_history.text, print_history, print_sp)
            # ai_output = interact_with_gemini(chat, print_history.text) # 与AI交互
            ai_output_command = extract_command(ai_output)
            print_history.clear()

            if ai_output_command:
                try:
                    current_command.text = ai_output_command # 将AI输出的命令赋值给当前命令
                    system_output = current_command.execute() # 执行当前命令
                    spoke(system_name)
                    slow_print.slow_print(system_output) # 打印命令执行结果
                    print_history.add_line(system_output)
                except Exception as e:
                    spoke()
                    slow_print.slow_print(str(e)) # 打印异常信息
                    print_history.add_line(str(e))

            else:
                control_on_user = True


if __name__ == "__main__":
    main()
