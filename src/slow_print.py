import time

def slow_print(text, delay=0.002, enter=True):
    """逐字打印文本，每个字之间延时 delay 秒"""
    for char in text:
        if char not in ("*", "`"):  # 检查字符是否是要跳过的字符
            print(char, end='', flush=True)
            time.sleep(delay)
    if enter:
        print()  # 打印换行