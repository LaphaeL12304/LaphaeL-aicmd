#!/usr/bin/env python3

# This program is named 'LaphaeLaicmd-linux', it allows chat AI to execute commands on the user's Linux system.
# 该程序名为'LaphaeLaicmd-linux'，它允许聊天AI在用户的Linux系统上执行命令。
# Copyright (C) 2024 LaphaeL
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import os
import getpass
import platform
import distro

from . import globals as gl
from . import config as cf
from . import utils as ut
from . import interact_AI as ai
from . import match_instruct
from . import execute_cmd


def main():
    """
    主函数 - Main function
    """

    # 打印初始化信息 - Print initialization information
    ut.print_spoker(record=False)
    print("正在初始化...")

    # 获取系统信息 - Get system information
    print("正在获取系统信息...")

    gl.pwd_path = os.getcwd()
    result = getpass.getuser()
    cf.user_name = result.replace('\n', '')
    cf.system_version = distro.version(pretty=True)
    cf.system_name = distro.name()

    # 读取文件 - Read files
    print("正在获取配置文件...")

    if cf.instruction_prompt == '':
        sys.exit("'instruct_prompt'为空")
    elif cf.custom_instruct == '':
        cf.custom_instruct = "None"

    # 配置AI - Configure AI
    print("正在尝试连接到\"" + cf.ai_name + "\"...")

    init_prompt = cf.program_name + \
        ": Here is the custom instruction you should follow in the subsequent conversation:{\n" + \
        cf.custom_instruct + "}\n" + \
        "Here is some basic information about the user's system:{\n" + \
        "System version: " + cf.system_version + "\n" + \
        "Operating path: " + gl.pwd_path + "\n" + \
        "User name: " + cf.user_name + "\n}" + \
        "If you understand the instructions above, please reply '准备就绪'"

    # 获取AI类 - Get AI class
    try:
        chat_ai_class = ai.get_ai_class()
        chat_ai = chat_ai_class(api_key=cf.My_key, instruction_prompt=cf.instruction_prompt, init_prompt=init_prompt)
    except Exception as e:
        sys.exit("获取AI类失败：" + str(e))

    if not chat_ai.ready:
        sys.exit("连接到\"" + cf.ai_name + "\"失败")

    # 初始化完成 - Initialization complete
    ut.print_spoker(record=False)
    print("连接成功! \"" + cf.ai_name + "\"已经理解程序要求")
    print("\"" + cf.program_name + "\"已准备就绪!")

    gl.send_buffer = ""

    print('_' * os.get_terminal_size().columns, end="\n\n")


    # 主循环 - Main loop
    control_on_user = True
    global user_input, user_input_sent
    while True:
        if control_on_user:
            ut.print_spoker(ut.set_color(cf.user_name, cf.user_name_color), raw_name=cf.user_name, end="")
            user_input = input()

            if user_input.startswith('/'):
                gl.send_buffer += user_input + '\n'
                match_instruct.match_instruction(user_input)

            elif user_input:
                user_input_sent = False
                control_on_user = False

        else:
            if user_input_sent:
                user_input = ""

            ai_output = chat_ai.interact(user_input, gl.send_buffer)
            user_input_sent = True
            gl.send_buffer = ""
            ai_output_command = ut.extract_command(ai_output)

            if ai_output_command:
                try:
                    system_output = execute_cmd.execute_command(ai_output_command)  # 执行此命令 - Execute this command
                    gl.send_buffer += system_output

                except ValueError as e:
                    ut.print_spoker()
                    ut.print_and_record(str(e))  # 打印异常信息 - Print exception information
                    control_on_user = True

                except Exception as e:
                    ut.print_spoker()
                    ut.print_and_record(str(e))  # 打印异常信息 - Print exception information

            else:
                control_on_user = True

if __name__ == '__main__':
    main()