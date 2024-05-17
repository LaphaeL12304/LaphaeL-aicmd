#!/usr/bin/env python3

# This program is named 'LaphaeLaicmd-linux', it allows chat AI to execute commands on the user's Linux system.
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


from . import globals as gl
from . import config as cf
from . import utils as ut
from . import interact_AI as ai
from . import match_instruct
from . import execute_cmd



def main():


    # 打印初始化信息
    ut.print_spoker(record=False)
    print("正在初始化...")


    # 获取系统信息
    print("正在获取系统信息...")

    try:
        gl.pwd_path = execute_cmd.execute_command("pwd", False, False)
        gl.ls_home = execute_cmd.execute_command("ls", False, False)
        result = execute_cmd.execute_command("whoami", False, False)
        cf.user_name = result.replace('\n', '')
        result = execute_cmd.execute_command("lsb_release -a", False, False)
    except Exception as e:
        sys.exit("获取信息失败："+ str(e))

    for line in result.split('\n'):
            if 'description:' in line.lower():
                # 获取干净的系统信息
                cf.system_version = line.split(':')[1].strip()
                break

    cf.system_name = cf.system_version.split()[0]


    # 读取文件
    print("正在获取配置文件...")

    try:
        instruction_prompt = ut.read_file(cf.instruction_prompt_path)
        custom_instruct = ut.read_file(cf.custom_instruct_path)
    except Exception as e:
        sys.exit("读取文件失败："+ str(e))

    if instruction_prompt == '':
        sys.exit(f"{cf.instruction_prompt_path}文件为空")
    elif custom_instruct == '':
        sys.exit(f"{cf.custom_instruct_path}文件为空")


    # 配置AI
    print("正在尝试连接到\"" + cf.ai_name + "\"...")

    prompt = "Here is how you should response:{\n" + \
        instruction_prompt + \
        "\n}\nHere is the custom instruction you should follow:{\n" + \
        custom_instruct + \
        "如果你明白以上要求，请回复\"准备就绪\""

    chat_ai = ai.Chat_AI_gemini(api_key = cf.ai_API_key, instruction_prompt=prompt)

    if not chat_ai.ready:
        sys.exit("连接到\"" + cf.ai_name + "\"失败")
    

    # 初始化完成
    ut.print_spoker(record=False)
    print("连接成功! \"" + cf.ai_name + "\"已经理解程序要求")
    print("\"" + cf.program_name + "\"已准备就绪!")

    gl.history = ""

    print('_' * 80, end="\n\n")

    

    #主程序
    control_on_user = True
    global user_input, user_input_sent
    while True:

        if control_on_user:
            ut.print_spoker(ut.set_color(cf.user_name, cf.user_name_color), raw_name=cf.user_name, end="")
            user_input = input()

            if user_input.startswith('/'):
                gl.history += user_input + '\n'
                match_instruct.match_instruction(user_input)

            elif user_input:
                user_input_sent = False
                control_on_user = False

        else:
            if user_input_sent:
                user_input = ""

            ai_output = chat_ai.interact(user_input, gl.history)
            user_input_sent = True
            gl.history = ""
            ai_output_command = ut.extract_command(ai_output)

            if ai_output_command:
                try:
                    system_output = execute_cmd.execute_command(ai_output_command) # 执行此命令命令
                    if not system_output.replace(" ",""):
                        system_output = "执行成功\n"
                    gl.history += system_output # 将执行结果添加到历史记录中
                except Exception as e:
                    ut.print_spoker()
                    ut.print_and_record(str(e)) # 打印异常信息

            else:
                control_on_user = True



if __name__ == '__main__':
    main()
    
