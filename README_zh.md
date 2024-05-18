- # LaphaeLaicmd-linux

  - 让聊天AI可以在用户的计算机执行Linux命令

  ---

  # 简体中文 | [English](https://github.com/LaphaeL12304/LaphaeLaicmd-linux/blob/main/README.md)

  ## V1.2.1更新内容

  1. **新增支持ChatGPT！**
  2. 使用**poetry**虚拟环境工具打包和管理代码 (感谢来自[DataEraserC](https://github.com/DataEraserC)[Sacabambaspis](https://github.com/DataEraserC)贡献的代码)
  3. 更好的用户交互逻辑
  4. 更改启动逻辑：`~/.bashrc`中`alias`语句已更改，详见下文**"安装"**部分

  > [!WARNING]
  >
  > - **注意！尽管此程序要求用户确认才能执行Linux命令，但很难保证不会出什么bug，因此请勿在有重要资料的系统上运行此程序**
  > - 此程序目前仍处于**早期阶段**，bug还很多，并且只测试了Ubuntu 22.04 LTS发行版上的运行

  ## 特性

  - 在Linux终端输入`aicmd`即可启动
  - 自动捕获AI响应中的Linux命令
  - 执行命令前向用户确认
  - AI可分步骤执行复杂任务
  - 目已支持Gemini与ChatGPT，未来考虑支持Ollama本地模型
  - 目前只有中文界面，正在考虑加入其他语言
  
  ## 安装
  
  #### 下载程序：
  
  - [Github下载链接](https://github.com/LaphaeL12304/LaphaeLaicmd-linux/archive/refs/heads/main.zip)
  
  #### Python依赖模块：
  
  1. pexpect模块
     - 此模块用于执行Linux命令，可以通过以下命令安装：  
       `pip install pexpect`
  2. google-generativeai模块
     - 如果使用Gemini模型，则需要使用这个模块，可以通过以下命令安装：  
       `pip install -q -U google-generativeai`
  3. openai模块
     - 如果使用ChatGPT模型，则需要使用这个模块，可以通过以下命令安装：  
       `pip install openai`
  
  #### 添加Linux自定义命令：
  
  1. 在Linux终端执行以下命令以打开文件：  
     `nano ~/.bashrc`
  2. 在文件末尾添加自定义命令：  
     `alias aicmd="python3 此程序所在的目录/LaphaeLaicmd-linux/main.py"`
  3. 运行以下命令以应用更改：
     `source ~/.bashrc`
  
  #### 设置API：
  
  1. 打开`src/config.py`文件
  2. 找到`src/config.py`中的**第63行**，将`api_key`更改为你的API (Gemini的API可以从 google aistudio 免费获取)  
     `api_key = "Your-API-Key"`
  
  #### 启动：
  
  - 从终端输入`aicmd`即可启动程序
  - 请确保你的网络环境可以连接到AI
  
  #### 更换AI模型：
  
  - 默认模型为gpt-4o，如需更换模型则：
  
  1. 打开`src/config.py`文件
  2. 找到`src/config.py`中的**第55-57行**，根据注释提示将`ai_class`，`ai_name`，`ai_model`更换为你选择的模型
  
  ## 使用教程
  
  - 输入你的需求后自动发送给AI
  - AI的回复如果带着Linux命令，则需要用户进行`[Y/n]`确认 (直接回车也会执行)
  
  > [!TIP]
  >
  > 试试输入`帮我安装Chrome`；`在桌面创建个文件夹`；`帮我解决这个问题`；`我的显卡是什么型号？`
  
  - 输入以**'/'**开始的文本以执行程序指令：
    - 打印帮助文本：  
      `/` or `/help` or `/帮助` 
    - 退出程序：  
      `/exit` or `/退出`
    - 打印即将发送给AI的内容 (上次发送之后的历史记录) ：  
      `/content` or `/内容`
    - 清除即将发送给AI的内容：  
      `/clear` or `/清空`
    - 手动执行某命令，e.g. **"example"**：  
      `/cmd example`
  
  ## 已知问题
  
  - 无法转义带有引号命令 (包括单引号和双引号)  
    E.g. : `echo 'print(\"Hello\")'`，无法正常输出
  
  ---
  
  ## 链接
  
  - [Github仓库](https://github.com/LaphaeL12304/LaphaeLaicmd-linux)
  - [Bilibili](https://space.bilibili.com/454973135?spm_id_from=333.337.0.0)
  - [qq讨论群](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=hE0n_WloYeCndEoIMKjXK5V13yFhswDC&authKey=escV%2FqTpM7dCaNduH1ibLzhp1rIxMCE%2FiMH07XES9Z3yXC9iWbgWkW4h7nPZ7hHJ&noverify=0&group_code=893275911)
