# 简介
* **注意！尽管程序要求用户确认指令才能执行，但很难保证不会出什么bug，因此请不要在有重要资料的系统上运行**
* aicmd-linux的目标是使用户摆脱敲命令，实现真正的自然语言操作linux系统
* 目前该程序处于**非常早期阶段**，bug还很多，并且只测试了Ubuntu 22.04.4 LTS发行版上的运行


# 特性
* 目前仅支持gemini
* 自动获取AI响应中的linux命令
* 执行前向用户确认


# 安装

## 依赖库：
  * ### pexpect库
  * 用于执行linux命令，可通过以下命令安装：
  * ```pip install pexpect```

  * ### google-generativeai库
  * 如果使用gemini模型，则需要使用这个库，可以通过以下命令安装：
  * ```pip install -q -U google-generativeai```

## 添加linux自定义命令：
  * ### 在linux终端执行以下命令打开文件：
  * ```nano ~/.bashrc```

  * ### 在文件末尾添加自定义命令：
  * ```alias aicmd="cd ~ && main.py在你计算机上的路径"```

  * ### 更新文件：
  * ```source ~/.bashrc```

## 设置API
 * 找到**main.py**中的第59行，将API改为你的gemini API（可以从google aistudio免费获取）
 * ```chat_ai.api = "Your-API-Key"```

## 启动
  * 从终端输入"aicmd"即可启动程序
  * 请确保你的网络环境可以连接到gemini
  * 输入 '/' 或 '/help' 或 '/帮助' 查看使用说明
  * 输入 '/exit' 或 '/退出' 以退出程序
  * 输入 '/cmd the_command' 以手动执行'the command'
  * 输入不以'/'开头的文本，则文本会自动发送给AI

# 更新内容: v1.1.1
 * 整理代码，初步模块化

# 已知bug
 * 运行`echo`命令时，如果内容包含小括号，即'('或')'，比如`echo ~/test.py "print("hello world")"`,那么执行时会报错
