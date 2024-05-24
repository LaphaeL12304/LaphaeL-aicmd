"""匹配指令 - Match Instructions"""

import sys

from . import globals as gl
from . import config as cf
from . import utils as ut
from . import execute_cmd

def match_instruction(instruction):
    """
    处理输入的指令 - Process input instructions
    
    :param instruction: 用户输入的指令 - User input instruction
    """
    if instruction.startswith('/cmd '):
        try:
            system_output = execute_cmd.execute_command(instruction[5:], False)  # 执行此命令 - Execute this command
            gl.send_buffer += system_output  # 将执行结果添加到历史记录中 - Add execution result to history
        except Exception as e:
            ut.print_spoker()
            ut.print_and_record(str(e))  # 打印异常信息 - Print exception information
    
    else:
        ut.print_spoker()

        match instruction:  # 如果用户输入以'/'开头，则匹配用户输入 - Match user input if it starts with '/'

            case "/exit" | "/退出":  # 退出程序 - Exit program
                print("正在退出程序...")
                sys.exit(0)

            case "/help" | "/帮助" | "/":  # 打印帮助文本 - Print help text
                ut.slow_print("这是帮助文本，暂时没写", record=False)
                gl.send_buffer += "#省略帮助文本\n"

            case "/content" | "/内容":  # 打印即将发送的内容 - Print content to be sent
                ut.slow_print("以下是历史记录：\n" + gl.send_buffer, record=False)
                gl.send_buffer += "#省略打印历史记录\n"

            case "/clear" | "/清空":  # 清空即将发送的内容 - Clear content to be sent
                gl.send_buffer = ""
                print("历史记录已清空")

            case _:  # 其他情况 - Other cases
                ut.print_and_record("无效指令")