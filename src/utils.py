"""其他函数 - Other Functions"""

import time
import sys
import re
import os

from . import config as cf
from . import globals as gl


def extract_command(text) -> str:
    """
    匹配被"///"包裹的文本 - Match text enclosed by "///"
    
    :param text: 输入文本 - Input text
    :return: 匹配的命令或空字符串 - Matched command or empty string
    """
    pattern = r'///(.*?)///'
    match = re.search(pattern, text)  # 查找第一个匹配项 - Find the first match
    return match.group(1) if match else ""  # 如果没有匹配项则返回空 - Return empty if no match


def set_color(text, color: str="37") -> str:
    """
    转为带颜色的字符串 - Convert text to colored string
    
    :param text: 输入文本 - Input text
    :param color: 颜色代码 - Color code
    :return: 带颜色的字符串 - Colored string
    """
    return f"\033[{color}m" + text + "\033[0m"


def print_and_record(text, end='\n'):
    """
    打印文本并记录到历史 - Print text and record to history
    
    :param text: 输入文本 - Input text
    :param end: 结束符 - End character
    """
    print(text, end=end)
    gl.send_buffer += text + end


def slow_print(text, print_time: float=0.10, max_delay: float=0.01, end='\n', record: bool=True):
    """
    逐字打印文本 - Print text character by character
    
    对于流式传输时会'少次多量'地输出文本的AI(例如Gemini)，这个函数可以流畅的逐字打印输出
    但对于每次只输出没几个字符的AI(例如ChatGPT)，这个函数会降低打印速度，因此不推荐此情况下使用
    For AIs that output text in large chunks (e.g., Gemini), this function can smoothly print character by character.
    However, for AIs that output only a few characters at a time (e.g., ChatGPT), this function will slow down the print speed, so it is not recommended in such cases.
    
    :param text: 输入文本 - Input text
    :param print_time: 打印时间 - Print time
    :param max_delay: 最大延迟 - Maximum delay
    :param end: 结束符 - End character
    :param record: 是否记录 - Whether to record
    """
    delay = (print_time / len(text)) if len(text) > 5 else 0
    if delay > max_delay:
        delay = max_delay

    for char in text:
        print(char, end='', flush=True)
        if delay:
            time.sleep(delay)

    print("", end=end)

    if record:
        gl.send_buffer += text + end


_last_spoker = ""
def print_spoker(spoker: str | None=None, raw_name: str | None=None, end='', record: bool=True):
    """
    打印发言人 - Print speaker
    
    :param spoker: 发言人 - Speaker
    :param raw_name: 原始名称 - Raw name
    :param end: 结束符 - End character
    :param record: 是否记录 - Whether to record
    """
    global _last_spoker
    
    if spoker is None:
        spoker = set_color(cf.program_name, cf.program_name_color)
        raw_name = cf.program_name
    
    if _last_spoker != spoker:
        print(spoker + ": ", end=end)
        _last_spoker = spoker

    if record:
        if raw_name is not None:
            gl.send_buffer += raw_name + ": " + end
        else:
            gl.send_buffer += spoker + ": " + end


def confirm(printstr: str="Do you agree?") -> bool:
    """
    打印[Y/n]确认界面 - Print [Y/n] confirmation interface
    
    :param printstr: 提示字符串 - Prompt string
    :param program_name: 程序名称 - Program name
    :return: 用户确认结果 - User confirmation result
    """
    print_spoker()
    print_and_record(printstr + "[Y/n]", end="")

    result = input()
    gl.send_buffer += result + "\n"

    return True if result.lower() == 'y' or (not result) else False  # 如果输入y或无输入，则返回True - Return True if input is 'y' or empty


def read_file(file_path):
    """
    读取文件 - Read file
    
    :param file_path: 文件路径 - File path
    :return: 文件内容 - File content
    :raises Exception: 如果文件不存在或读取失败 - If file does not exist or reading fails
    """
    if not os.path.exists(file_path):
        raise Exception("File do not exist") from None
    else:
        try:
            # 打开文件，指定相对路径 - Open file with specified relative path
            with open(file_path, 'r', encoding='utf-8') as file:
                # 返回文件内容到字符串 - Return file content as string
                return file.read()
        except Exception as e:
            raise Exception(str(e)) from None