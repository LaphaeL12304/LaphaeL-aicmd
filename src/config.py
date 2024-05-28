"""配置文件"""

import os
import shutil
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

# TODO: 将默认配置文件打包到site-packages/LaphaeLaicmd/data/
# origin_resource_dir = os.path.dirname(__file__)

# 默认从环境变量读取数据文件夹的位置 不存在则回退到默认的位置~/.config/LaphaeLaicmd
resource_dir = os.getenv('laphaelaicmd_linux_config_dir', os.path.join('~', '.config', 'LaphaeLaicmd'))
resource_dir = os.path.expanduser(resource_dir)

if os.path.exists(os.path.join(resource_dir,"data")):
    pass
else:
    os.makedirs(os.path.join(resource_dir,"data"))

# 获取AI设置 若不存在则创建
ai_settings_path = os.path.join(resource_dir, "data", "AI_settings.toml")
if os.path.exists(ai_settings_path):
    pass
else:
    shutil.copy(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"data","AI_settings.toml"), os.path.join(resource_dir,"data"))

# 获取其他设置 若不存在则创建
config_path = os.path.join(resource_dir, "data", "config.toml")
if os.path.exists(config_path):
    pass
else:
    shutil.copy(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"data","config.toml"), os.path.join(resource_dir,"data"))

ai_settings = load_toml_config(ai_settings_path)
config = load_toml_config(config_path)

ai_name = get_config_value(ai_settings, "info", "select_ai")
if ai_name is not None:
    ai_model = get_config_value(ai_settings, f"info.{ai_name}", "model")
    My_key = get_config_value(ai_settings, f"info.{ai_name}", "api_key")
else:
    ai_model = None
    My_key = None

instruction_prompt = get_config_value(ai_settings, "prompt", "text")
custom_instruct = get_config_value(ai_settings, "custom_instruct", "text")


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


if __name__ == "__main__":
    print("AI Name:", ai_name)
    print("API Key:", My_key)
    print("Model:", ai_model)
    print("color:", ai_name_color)
