"""匹配指令"""

import pexpect
import sys

import globals as gl
import config as cf
import utils as ut
import execute_cmd


def match_instruction(instruction):
    """处理输入的指令"""

    if instruction.startswith('/cmd '):
        try:
            system_output = execute_cmd.execute_command(instruction[5:]) # 执行此命令命令
            if not system_output.replace(" ",""):
                system_output = "执行成功\n"
            gl.history += system_output # 将执行结果添加到历史记录中
        except Exception as e:
            ut.print_spoker()
            ut.print_and_record(str(e)) # 打印异常信息
    
    else:
        ut.print_spoker()

        match instruction: # 如果用户输入以'/'开头，则匹配用户输入

            case "/exit" | "/退出": # 退出程序
                print("正在退出程序...")
                sys.exit(0)

            case "/help" | "/帮助" | "/": # 打印帮助文本
                ut.slow_print("这是帮助文本，暂时没写", record=False)
                gl.history += "#省略帮助文本\n"

            case "/history" | "/历史": # 打印历史记录
                ut.slow_print("以下是历史记录：\n" + gl.history, record=False)
                gl.history += "#省略打印历史记录\n"

            case "/clear" | "/清空": # 清空历史记录
                gl.history = ""
                print("历史记录已清空")

            case _: # 其他情况
                ut.print_and_record("无效指令")