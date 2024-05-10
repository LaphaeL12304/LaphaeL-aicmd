import slow_print
import _print_spoker as sp
def confirm(printstr = "是否同意?", program_name = ""):
    """打印[Y/n]确认界面"""
    sp.print_spoker(program_name)
    slow_print.slow_print(printstr, enter=False)
    t = "[Y/n]"
    result = input(t)
    return True if result.lower() == 'y' or (not result) else False # 如果输入y或无输入，则返回True