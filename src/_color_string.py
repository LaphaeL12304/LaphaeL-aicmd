"""
带颜色的字符串
"""

def set_color(text, color="white", state="normal"):
    match color.lower():
        case "black":
            color_text = "\033[30;1m"
        case "red":
            color_text = "\033[31;1m"
        case "green":
            color_text = "\033[32;1m"
        case "yellow":
            color_text = "\033[33;1m"
        case "blue":
            color_text = "\033[34;1m"
        case "purple":
            color_text = "\033[35;1m"
        case "cyan":
            color_text = "\033[36;1m"
        case "white":
            color_text = "\033[37;1m"
        case _:
            color_text = "\033[37;1m"

    match state.lower():
        case "normal":
            state_text = ""
        case "bold":
            state_text = "\033[1m"
        case "underline":
            state_text = "\033[4m"
        case _:
            state_text = ""

    return color_text + state_text + text + "\033[0m"


class Color_str():

    def __init__(self, text, color="white", state="normal"):
        self.raw = text
        self.color = color
        self.state = state
        self.text = set_color(text, color, state)

    def __str__(self):
        return self.text