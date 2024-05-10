import _color_string as cs


class chat_AI():
    def __init__(self, raw_name, model):
        self.raw_name = raw_name
        self.name = cs.Color_str(self.raw_name, "blue", "bold")
        self.api = None
        self.model = model
    
    def initialize(self):
        pass

    def interact(self, content, history):
        pass