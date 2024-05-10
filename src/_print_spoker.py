"""打印发言人"""
import slow_print
import record_history

class print_spoker():
    def __init__(self, default_name):
        self.default_name = default_name
        self.last_printer = None
    def __call__(self, name=None):
        """打印发言人"""
        if name is None:
            name = self.default_name
        if name != self.last_printer:
            slow_print.slow_print(name.text + ": ", enter=False)
        self.last_printer = name