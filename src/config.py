"""配置参数"""

import os


# 定义字体颜色

# 文本颜色
# 30：黑色
# 31：红色
# 32：绿色
# 33：黄色
# 34：蓝色
# 35：洋红色
# 36：青色
# 37：白色
# 背景颜色
# 40：黑色背景
# 41：红色背景
# 42：绿色背景
# 43：黄色背景
# 44：蓝色背景
# 45：洋红色背景
# 46：青色背景
# 47：白色背景
# 格式
# 0：重置所有属性
# 1：加粗
# 4：下划线
# 5：闪烁
# 7：反显
# 8：隐藏

# 打印的发言人名称颜色
program_name_color = "35;1"
user_name_color = "32;1"
system_name_color = "33;1"
ai_name_color = "34;1"

# AI输出文本打印的颜色
ai_print_color = "37;1"


# 定义初始名称
program_name = "AIcmd"
user_name = "User"
system_name = "System"
ai_name = "Gemini"

system_version = "System version unkown"


# 设置AI信息
ai_model = "gemini-pro"
ai_API_key = "Your-API-Key"


# 定义路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
instruction_prompt_path = os.path.join(project_root, "data", "instruction_prompt.txt")
custom_instruct_path = os.path.join(project_root, "data", "custom_instruct.txt")