import pexpect
import getpass
import _print_spoker as sp
import _color_string
import _user_confirm

password_prompt = 'password:'
password_prompt_zh = '密码：' # 系统的密码提示符

class Command():

    def __init__(self, program_name):
        self.text = ""
        self.program_name = program_name

    def replace_home(self, home_path):
        self.text = self.text.replace('~', home_path) # 将'~'替换为当前目录

    def execute(self, need_confirm = True):
        """执行命令"""
        # 如果命令包含sudo，则需要确认
        if ('sudo' in self.text) or need_confirm:
            confirm_state = _user_confirm.confirm("是否执行命令\"" + _color_string.set_color(self.text, "purple", "bold") + "\"？", self.program_name)
            if not confirm_state:
                raise ValueError("用户拒绝执行命令。")
        
        child = pexpect.spawn(f'/bin/bash -c "{self.text}"', encoding='utf-8')
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
                        else:
                            t = "请输入管理员密码："
                            password = getpass.getpass(t)
                        passretry = True
                        child.sendline(password)
                    case 2:  # EOF，命令执行完成
                        return child.before.strip()
                    case 3:  # 超时
                        raise TimeoutError("命令执行超时。")

        except pexpect.exceptions.EOF: # 子进程被异常终止
            raise EOFError("子程序被异常终止。") from None
        except Exception as e: # 发生异常
            raise Exception("发生异常"+str(e)) from e