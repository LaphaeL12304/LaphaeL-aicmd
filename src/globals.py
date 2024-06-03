"""全局变量 - Global variables"""
import gettext
import locale
import os


send_buffer = "" # 即将发送给AI的内容 - Content to be sent to AI

pwd_path = ""


def setup_i18n(current_locale="en_US"):
    """
    设置语言 - Set language

    :param current_locale: 系统默认的地区设置，可能需要处理一下格式以适配gettext
     - System's default language, may require normalization for gettext
    """
    
    current_dir = os.path.dirname(__file__)
    locale_path = os.path.join(current_dir, "../locales")
    locale_path = os.path.normpath(locale_path)

    mo_path = os.path.join(locale_path, current_locale, 'LC_MESSAGES', 'messages.mo')

    try:
        language = gettext.translation('messages', localedir=locale_path, languages=[current_locale], fallback=True)
        language.install()

    except FileNotFoundError:
        # 找不到指定的语言文件，加载默认语言(en_US) - Language not found, fallback to English
        logging.warning(f"Language file for {current_locale} not found. Falling back to English (US).")
        language = gettext.translation('messages', localedir=locale_path, languages=['en_US'], fallback=True)
        language.install()

    except Exception as e:
        print("Error loading the .mo file:", e)
        _ = lambda x: x


def translate(text):
    return _(text)