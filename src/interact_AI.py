"""与AI交互 - Interacting with AI"""

import google.generativeai as genai
from openai import OpenAI
import requests
import os

from . import config as cf
from . import utils as ut
from . import globals as gl
from . import execute_cmd


# 设置代理 - Set proxy
os.environ['ALL_PROXY'] = ""
os.environ['all_proxy'] = ""


class Chat_AI():
    """所有AI的基类 - Base class for all AIs"""

    def __init__(self, name=cf.ai_name, model=cf.ai_model, \
                 print_color=cf.ai_name_color, api_key=None, instruction_prompt=""):
        """
        初始化Chat_AI类 - Initialize Chat_AI class

        :param name: AI的名称 - Name of the AI
        :param model: AI的模型 - Model of the AI
        :param print_color: 打印颜色 - Print color
        :param api_key: API密钥 - API key
        :param instruction_prompt: 指令提示 - Instruction prompt
        """
        self.name = name
        self.color_name = ut.set_color(name, print_color)
        self.api_key = api_key
        self.model = model
        self.instruction_prompt = instruction_prompt
        self.ready = False


    def interact(self, content, history):
        """
        与AI进行交互 - Interact with the AI

        :param content: 用户输入的内容 - User input content
        :param history: 交互历史 - Interaction history
        """
        pass


class Chat_AI_gemini(Chat_AI):
    """Gemini AI"""

    def __init__(self, name=cf.ai_name, model=cf.ai_model, \
                 print_color=cf.ai_name_color, api_key=None, instruction_prompt="", init_prompt="如果你能明白我的要求，请回复'准备就绪'"):
        """
        初始化Chat_AI_gemini类 - Initialize Chat_AI_gemini class

        :param name: AI的名称 - Name of the AI
        :param model: AI的模型 - Model of the AI
        :param print_color: 打印颜色 - Print color
        :param api_key: API密钥 - API key
        :param instruction_prompt: 指令提示 - Instruction prompt
        :param init_prompt: 初始化提示 - Initialization prompt
        """
        super().__init__(name, model, print_color, api_key)
        if self.api_key is None:
            raise Exception("API key not identified")

        # 初始化Gemini AI - Initialize Gemini AI
        genai.configure(api_key=self.api_key)
        self.genai_model = genai.GenerativeModel(self.model)
        self.chat = self.genai_model.start_chat(history=[])

        # 打印AI名称 - Print AI name
        ut.print_spoker(self.color_name, raw_name=self.name, end="", record=False)

        # 打印AI的输出 - Print AI output
        response = self.chat.send_message(instruction_prompt + init_prompt, stream=True)
        ai_text = ""

        for chunk in response:
            ut.slow_print(ut.set_color(chunk.text, cf.ai_print_color), 0.50, end="", record=False)
            ai_text += chunk.text
        print("")

        # 判断AI是否准备就绪 - Check if AI is ready
        if ("准备就绪" in ai_text.strip().lower()) or ("ready" in ai_text.strip().lower()):
            self.ready = True


    def interact(self, content, history):
        """
        与Gemini API进行对话, 并利用流式传输逐字打印回答 - Interact with Gemini API and print responses character by character

        :param content: 用户输入的内容 - User input content
        :param history: 交互历史 - Interaction history
        """
        # 打印AI名称 - Print AI name
        ut.print_spoker(self.color_name, raw_name=self.name, end="\n")

        message = "AIcmd history: {" + history + "}"

        if content:
            message += "\nPlease answer the user's input: {" + content + "}"

        response = self.chat.send_message(message, stream=True)
        ai_text = ""

        # 逐字打印AI的回答 - Print AI response character by character
        for chunk in response:
            ut.slow_print(ut.set_color(chunk.text, cf.ai_print_color), 0.50, end="", record=False)
            ai_text += chunk.text
        print("")

        gl.send_buffer += "#省略AI的回答"
        return ai_text.strip()


class Chat_AI_GPT(Chat_AI):
    """ChatGPT AI"""

    def __init__(self, name=cf.ai_name, model=cf.ai_model, \
                 print_color=cf.ai_name_color, api_key=None, instruction_prompt="", init_prompt="如果你能明白我的要求，请回复'准备就绪'"):
        """
        初始化Chat_AI_GPT类 - Initialize Chat_AI_GPT class

        :param name: AI的名称 - Name of the AI
        :param model: AI的模型 - Model of the AI
        :param print_color: 打印颜色 - Print color
        :param api_key: API密钥 - API key
        :param instruction_prompt: 指令提示 - Instruction prompt
        :param init_prompt: 初始化提示 - Initialization prompt
        """
        super().__init__(name, model, print_color, api_key, instruction_prompt)
        if self.api_key is None:
            raise Exception("API key not identified")

        # 初始化OpenAI API - Initialize OpenAI API
        self.client = OpenAI(api_key=self.api_key)
        self.instruction_prompt = instruction_prompt
        self.client_history = [{"role": "system", "content": self.instruction_prompt}]

        # 打印AI名称 - Print AI name
        ut.print_spoker(self.color_name, raw_name=self.name, end="", record=False)

        self.client_history.append({"role": "user", "content": init_prompt})

        # 打印AI的输出 - Print AI output
        ai_text = self._initialize_ai(init_prompt)
        print("")

        # 判断AI是否准备就绪 - Check if AI is ready
        if ("准备就绪" in ai_text.strip().lower()) or ("ready" in ai_text.strip().lower()):
            self.ready = True


    def _initialize_ai(self, init_prompt):
        """
        初始化AI - Initialize AI

        :param init_prompt: 初始化提示 - Initialization prompt
        :return: AI的响应文本 - AI response text
        """
        send_message = self.client_history.copy()
        send_message.append({"role": "user", "content": init_prompt})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=send_message,
            stream=True,
        )
        ai_text = ""
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content is not None:
                print(ut.set_color(content, cf.ai_print_color), end="", flush=True)
                ai_text += content

        self.client_history.append({'role': 'assistant', 'content': ai_text.strip()})
        return ai_text.strip()


    def interact(self, content, history):
        """
        与ChatGPT API进行对话，并利用流式传输逐字打印回答 - Interact with ChatGPT API and print responses character by character

        :param content: 用户输入的内容 - User input content
        :param history: 交互历史 - Interaction history
        """
        # 打印AI名称 - Print AI name
        ut.print_spoker(self.color_name, raw_name=self.name, end="\n")

        message = "AIcmd history: " + str(history)

        if content:
            message += "\nPlease answer the user's input: " + content

        self.client_history.append({"role": "user", "content": message})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.client_history,
            stream=True
        )
        ai_text = ""

        # 逐字打印AI的回答 - Print AI response character by character
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content is not None:
                print(ut.set_color(content, cf.ai_print_color), end="", flush=True)
                ai_text += content

        print("")
        gl.send_buffer += "#省略AI的回答"
        self.client_history.append({'role': 'assistant', 'content': ai_text.strip()})
        return ai_text.strip()


def get_ai_class():
    """
    获取AI类 - Get AI class

    :return: AI类 - AI class
    """
    match cf.ai_name:
        case "ChatGPT":
            return Chat_AI_GPT
        case "Gemini":
            return Chat_AI_gemini
        case _:
            raise ValueError("Unknown AI class specified in config.py")