"""配置文件 - Configurations"""

import os
import shutil
import toml
import polib
import gettext
import locale
import pkg_resources

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

def set_permissions_recursively(path, dir_mode=0o755, file_mode=0o644):
    # 遍历指定路径下的所有文件和目录
    for root, dirs, files in os.walk(path):
        # 设置目录的权限
        for d in dirs:
            os.chmod(os.path.join(root, d), dir_mode)
        # 设置文件的权限
        for f in files:
            os.chmod(os.path.join(root, f), file_mode)

def ensure_resource_existence(resource_directory: str, target_relative_path: str, source_packaged_path: str):
    # 确保资源文件夹存在
    expanded_resource_directory = os.path.expanduser(resource_directory)
    if not os.path.exists(expanded_resource_directory):
        os.makedirs(expanded_resource_directory,mode=0o755)
    
    # 构造目标路径
    target_path = os.path.join(expanded_resource_directory, target_relative_path)
    
    # 检查目标路径是否存在
    if not os.path.exists(target_path):
        # 判断是文件还是文件夹
        if os.path.isfile(source_packaged_path):
            # 复制文件
            shutil.copy2(source_packaged_path, target_path)
        elif os.path.isdir(source_packaged_path):
            # 复制文件夹
            shutil.copytree(source_packaged_path, target_path)
        else:
            # 原始路径既不是文件也不是文件夹，抛出异常或处理错误
            raise FileNotFoundError(f"The source packaged resource '{source_packaged_path}' does not exist.")

def overwrite_resource(resource_directory: str, target_relative_path: str, source_packaged_path: str):
    # 确保资源文件夹存在
    expanded_resource_directory = os.path.expanduser(resource_directory)
    if not os.path.exists(expanded_resource_directory):
        os.makedirs(expanded_resource_directory, mode=0o755)
    
    # 构造目标路径
    target_path = os.path.join(expanded_resource_directory, target_relative_path)
    
    # 判断是文件还是文件夹
    if os.path.isfile(source_packaged_path):
        # 如果是文件，直接覆盖
        shutil.copy2(source_packaged_path, target_path)
    elif os.path.isdir(source_packaged_path):
        # 如果是文件夹，先尝试删除目标文件夹（如果存在），然后复制
        if os.path.exists(target_path):
            shutil.rmtree(target_path)  # 强制删除目标文件夹及其内容
        shutil.copytree(source_packaged_path, target_path)
    else:
        # 原始路径既不是文件也不是文件夹，抛出异常或处理错误
        raise FileNotFoundError(f"The source packaged resource '{source_packaged_path}' does not exist.")

def compile_po_to_mo(po_path: str, mo_path: str):
    """  
    使用Polib库将.po文件编译为.mo文件。
  
    Args:
        po_path (str): .po文件的路径。
        mo_path (str): 输出的.mo文件的路径。
  
    Returns:
        None: 函数不返回任何值，但会生成.mo文件。
  
    Raises:
        IOError: 如果无法读取或写入文件。
        其他可能的异常: Polib库可能抛出的其他异常。
    """
    try:  
        print(f"Compiling {po_path} to {mo_path}...")
        # 加载.po文件
        po = polib.pofile(po_path)

        # 将.po文件保存为.mo文件
        po.save_as_mofile(mo_path)

        print(f"Compiled {mo_path} successfully.")

    except IOError as e:
        print(f"IOError: {e} when compiling {po_path} to {mo_path}")

    except Exception as e:
        print(f"ErrorOccur: {e} when compiling {po_path} to {mo_path}")

# 默认从环境变量读取数据文件夹的位置 不存在则回退到默认的位置~/.config/LaphaeLaicmd
resource_dir = os.getenv('laphaelaicmd_linux_config_dir', os.path.join('~', '.config', 'LaphaeLaicmd'))
resource_dir = os.path.expanduser(resource_dir)
resource_dir = os.path.abspath(resource_dir)
package_dir = pkg_resources.resource_filename(__name__,"")

# path to ensure in resource_dir
resource_required_ensure = ["data/","locales/"]
for resource_required_ensure_dir in resource_required_ensure:
    ensure_resource_existence(resource_dir, resource_required_ensure_dir, os.path.join(package_dir, resource_required_ensure_dir))

set_permissions_recursively(resource_dir, dir_mode=0o755,file_mode=0o644)

def setup_i18n(locale: str="en_US"):
    """
    设置语言 - Set language

    :param current_locale: 系统默认的地区设置，可能需要处理一下格式以适配gettext
     - System's default language, may require normalization for gettext
    """
    # 一般来说，locale返回的是类似于'en_US.UTF-8'，需要简化为'en_US'
    current_locale = locale.split('.')[0] if locale else 'en_US'

    # ~/.config/LaphaeLaicmd/locales
    resource_locale_path = os.path.join(resource_dir, "locales")

    mo_dir = os.path.join(resource_locale_path, current_locale, 'LC_MESSAGES')
    mo_path = os.path.join(mo_dir, 'messages.mo')

    if not os.path.exists(mo_dir):
        os.makedirs(mo_dir, mode=0o755)

    if not os.path.exists(mo_path):
<<<<<<< HEAD
        try:
            po_path = os.path.join(locale_path, 'po_files', f'{current_locale}.po')
            print(f"Compiling {po_path} to {mo_path}...")
            subprocess.run(['msgfmt', po_path, '-o', mo_path], check=True)
            print(f"Compiled {mo_path} successfully.")
        except Exception as e:
            print(f"Failed to compile {po_path} to {mo_path}.")
=======
        po_path = os.path.join(resource_locale_path, 'po_files', f'{current_locale}.po')
        compile_po_to_mo(po_path,mo_path)
>>>>>>> b760228c8fc20038a6b5b2d99d6e5fd9936c80d4

    try:
        language = gettext.translation('messages', localedir=resource_locale_path, languages=[current_locale], fallback=True)
        language.install()

    except FileNotFoundError:
        # 找不到指定的语言文件，加载默认语言(en_US) - Language not found, fallback to English
        logging.warning(f"Language file for {current_locale} not found. Falling back to English (US).")
        if current_locale != 'en_US':
            setup_i18n('en_US')  # 设置为默认语言

    except Exception as e:
        print("Error loading the .mo file:", e)
        _ = lambda x: x

def translate(text):
    return _(text)


ai_settings_path = os.path.join(resource_dir, "data", "AI_settings.toml")
config_path = os.path.join(resource_dir, "data", "config.toml")
cli_outputs_path = os.path.join(resource_dir, "data", "_cli_outputs.toml")

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


# 打印的发言人名称颜色
program_name_color = get_config_value(config, "display", "program_name_color")
user_name_color = get_config_value(config, "display", "user_name_color")
system_name_color = get_config_value(config, "display", "system_name_color")
ai_name_color = get_config_value(config, "display", "ai_name_color")

# 语言选择
language_select = get_config_value(config, "display", "language")

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
