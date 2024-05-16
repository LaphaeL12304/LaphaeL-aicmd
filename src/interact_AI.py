"""与AI交互"""

import getpass
import google.generativeai as genai

from . import config as cf
from . import utils as ut
from . import globals as gl



class Chat_AI():
    """所有AI的基类"""

    def __init__(self, name=cf.ai_name, model=cf.ai_model,\
         print_color=cf.ai_name_color, api_key=None, instruction_prompt = ""):

        self.name = name
        self.color_name = ut.set_color(name, print_color)
        self.api_key = api_key
        self.model = model
        self.instruction_prompt = instruction_prompt
        self.ready = False
    

    def interact(self, content, history):
        pass



class Chat_AI_gemini(Chat_AI):
    """Gemini AI"""
    def __init__(self, name=cf.ai_name, model=cf.ai_model,\
         print_color=cf.ai_name_color, api_key=None, instruction_prompt = ""):

        super().__init__(name, model, print_color, api_key)
        if self.api_key is None:
            raise Exception("API key not identified")

        # 初始化Gemini AI
        genai.configure(api_key=self.api_key)
        self.genai_model = genai.GenerativeModel(self.model)
        self.chat = self.genai_model.start_chat(history=[])

        # 打印AI名称
        ut.print_spoker(self.color_name, raw_name=self.name, end="", record=False)

        # 打印AI的输出
        response = self.chat.send_message(instruction_prompt, stream=True)
        ai_text = ""

        for chunk in response:
            ut.slow_print(ut.set_color(chunk.text, cf.ai_print_color), 0.50, end="", record=False)
            ai_text += chunk.text
        print("")

        # 判断AI是否准备就绪
        if ("准备就绪" in ai_text.strip().lower()) or ("ready" in ai_text.strip().lower()):
            self.ready = True
            


    def interact(self, content, history):
        """与Gemini API进行对话, 并利用流式传输逐字打印回答"""

        # 打印AI名称
        ut.print_spoker(self.color_name, raw_name=self.name, end="\n")

        message = "History: {" + history + "}"

        if content:
            message += "\nPlease answer the user's input: {" + content + "}"

        response = self.chat.send_message(message, stream=True)
        ai_text = ""

        # 逐字打印AI的回答
        for chunk in response:
            ut.slow_print(ut.set_color(chunk.text, cf.ai_print_color), 0.50, end="", record=False)
            ai_text += chunk.text
        print("")

        gl.history += "#省略AI的回答"
        return ai_text.strip()
