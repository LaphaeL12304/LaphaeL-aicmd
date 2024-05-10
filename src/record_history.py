"""
历史记录
"""

class History():
    
    def __init__(self):
        self.text = "\33[0m"
    
    def __str__(self):
        return self.text
    
    def clear(self):
        self.text = "\33[0m"

    def add(self, text):
        self.text += text

    def add_line(self, text):
        self.text += text + "\n"
