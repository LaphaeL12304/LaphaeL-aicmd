"""配置文件"""

import os
import toml

def load_toml_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config = toml.load(file)
    return config

def save_toml_config(file_path, config):
    with open(file_path, 'w', encoding='utf-8') as file:
        toml.dump(config, file)

def get_config_value(config, section, key):
    try:
        # 支持嵌套的键
        keys = section.split('.') + [key]
        value = config
        for k in keys:
            value = value[k]
        return value
    except KeyError:
        return None

# 定义配置文件路径
config_dir = os.path.join(os.path.expanduser('~'), '.config', 'LaphaeLaicmd')
config_file = os.path.join(config_dir, 'config.ini')

# 检查配置文件目录是否存在，如果不存在则创建
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

# 检查配置文件是否存在，如果不存在则创建并写入初始数据
if not os.path.exists(config_file):
    # 使用configparser创建配置文件并写入初始数据
    config = configparser.ConfigParser()

    # 示例配置节和选项
    config['COLORS'] = {
        'program_name_color': '35;1',
        'user_name_color': '32;1',
        'system_name_color': '33;1',
        'ai_name_color': '34;1',
        'ai_print_color': '37;1',
    }
    config['NAMES'] = {
        'program_name': 'AIcmd',
        'user_name': 'User',
        'system_name': 'System',
    }
    config['AI'] = {
        'ai_class': 'Chat_AI_GPT',
        'ai_name': 'ChatGPT',
        'ai_model': 'gpt-4o',
        # 'ai_class': 'Chat_AI_gemini',
        # 'ai_name': 'Gemini',
        # 'ai_model': 'gemini-pro',

        'My_key': 'your_api_key',
    }
    config['other'] = {
        'system_version': 'System version unkown'
    }
    config['path'] = {
        'project_root': os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'instruction_prompt_path': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "instruction_prompt.txt"),
        'custom_instruct_path': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "custom_instruct.txt")
    }

    with open(config_file, 'w') as configfile:
        config.write(configfile)

# 读取配置文件中的数据
config = configparser.ConfigParser()
config.read(config_file)

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ai_settings_path = os.path.join(project_root, "data", "AI_settings.toml")
config_path = os.path.join(project_root, "data", "config.toml")

ai_settings = load_toml_config(ai_settings_path)
config = load_toml_config(config_path)

ai_name = get_config_value(ai_settings, "info", "select_ai")
if ai_name is not None:
    ai_model = get_config_value(ai_settings, f"info.{ai_name}", "model")
    My_key = get_config_value(ai_settings, f"info.{ai_name}", "api_key")
else:
    My_key = None

instruction_prompt = get_config_value(ai_settings, "prompt", "text")
custom_instruct = get_config_value(ai_settings, "custom_instruct", "text")


# 打印的发言人名称颜色
program_name_color = get_config_value(config, "display", "program_name_color")
user_name_color = get_config_value(config, "display", "user_name_color")
system_name_color = get_config_value(config, "display", "system_name_color")
ai_name_color = get_config_value(config, "display", "ai_name_color")

# AI输出文本打印的颜色
ai_print_color = get_config_value(config, "display", "ai_print_color")


# 定义初始名称
program_name = "AIcmd"
user_name = "User"
system_name = "System"
system_version = "System version unkown"

system_version = config['other']['system_version']

if __name__ == "__main__":
    print("AI Name:", ai_name)
    print("API Key:", my_key)
    print("Model:", ai_model)
    print("color:", ai_name_color)
