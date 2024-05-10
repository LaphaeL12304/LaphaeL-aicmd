import chat_with_AI
import google.generativeai as genai
import _print_spoker as sp
import slow_print
import _color_string as cs


class chat_AI_gemini(chat_with_AI.chat_AI):

    def __init__(self, raw_name, model):
        super().__init__(raw_name, model)

    def initialize(self):
        if self.api is None:
            raise Exception("API key not identified")
        genai.configure(api_key=self.api)
        self.genai_model = genai.GenerativeModel(self.model)
        self.chat = self.genai_model.start_chat(history=[])


    def interact(self, content, history, spoke):
        """与Gemini API进行对话，并利用流式传输逐字打印回答"""
        spoke(self.name)
        response = self.chat.send_message(content, stream=True)
        ai_text = ""
        for chunk in response:
            slow_print.slow_print(cs.set_color(chunk.text, state="bold"))
            ai_text += chunk.text
        history.add_line("#省略AI的回答")
        return ai_text.strip()
