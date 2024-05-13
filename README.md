# 简介
  * **注意！尽管程序要求用户确认指令才能执行，但很难保证不会出什么bug，因此请不要在有重要资料的系统上运行**
  * aicmd-linux的目标是使用户摆脱敲命令，实现真正的自然语言操作linux系统
  * 目前该程序处于**早期阶段**，bug还很多，并且只测试了Ubuntu 22.04.4 LTS发行版上的运行


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

## 设置API
  * 找到`config.py`中的第55行，将API改为你的gemini API（可以从google aistudio免费获取）
  * ```api_key = "Your-API-Key"```

## 启动
  * 从终端输入`aicmd`即可启动程序
  * 请确保你的网络环境可以连接到gemini
  * 输入 '/' 或 '/help' 或 '/帮助' 查看使用说明
  * 输入 '/exit' 或 '/退出' 以退出程序
  * 输入 '/cmd the_command' 以手动执行'the command'
  * 输入不以'/'开头的文本，则文本会自动发送给AI

# 更新内容 (v1.2.0)
  * 重新布局代码
  * execute_command()函数改为实时打印输出，并可以捕获并处理"[Y\n]"确认信息
  * 试试输入`帮我下载chrome`,`帮我删除vscode`等！

# 已知bug
