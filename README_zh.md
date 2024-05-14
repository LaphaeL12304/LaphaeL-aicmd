# LaphaeLaicmd-linux

- 让聊天AI可以在用户的计算机执行Linux命令

---

# 简体中文 | [English](https://github.com/LaphaeL12304/LaphaeLaicmd-linux/blob/main/README.md)

## V1.2.0更新内容

1. 支持捕获并处理需要`[Y/n]`交互的Linux命令
2. 执行命令改为实时打印结果，并非等待命令结束 (EOF)
3. 重新布局代码

> [!WARNING]
>
> - **注意！尽管此程序要求用户确认才能执行Linux命令，但很难保证不会出什么bug，因此请勿在有重要资料的系统上运行此程序**
> - 此程序目前仍处于**早期阶段**，bug还很多，并且只测试了Ubuntu 22.04.4 LTS发行版上的运行

## 特性

- 在Linux终端输入`aicmd`即可启动
- 自动捕获AI响应中的Linux命令
- 执行命令前向用户确认
- AI可分步骤执行复杂任务
- 目前仅支持Gemini，即将添加ChatGPT，未来考虑支持Ollama本地模型

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

#### 添加Linux自定义命令：

1. 在Linux终端执行以下命令以打开文件：  
   `nano ~/.bashrc`
2. 在文件末尾添加自定义命令：  
   `alias aicmd="cd ~ && python3 程序在你计算机上的路径/src/main.py"`
3. 运行以下命令以应用更改：
   `source ~/.bashrc`

#### 设置API：

- 找到`src/config.py`中的**第55行**，将`api_key`更改为你的 Gemini API (可以从 google aistudio 免费获取)  
  `api_key = "Your-API-Key"`

#### 启动：

- 从终端输入`aicmd`即可启动程序
- 请确保你的网络环境可以连接到Gemini

## 使用教程

- 输入你的需求后自动发送给AI
- AI的回复如果带着Linux命令，则需要用户进行`[Y/n]`确认 (直接回车也会执行)

> [!TIP]
>
> 试试输入**`帮我安装Chrome`**, `在桌面创建个文件夹`

- 输入以**'/'**开始的文本以执行程序指令：
  - 打印帮助文本：  
    `/` or `/help` or `/帮助` 
  - 退出程序：  
    `/exit` or `/退出`
  - 打印即将发送给AI的内容 (上次发送之后的历史记录) ：  
    `/history` or `/历史`
  - 清除即将发送给AI的内容：  
    `/clear` or `/清空`
  - 手动执行某命令，e.g. **"example"**：  
    `/cmd example`

## 已知问题

- 暂无

---

## 链接

- [Github仓库](https://github.com/LaphaeL12304/LaphaeLaicmd-linux)
- [Bilibili](https://space.bilibili.com/454973135?spm_id_from=333.337.0.0)
- [qq讨论群](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=hE0n_WloYeCndEoIMKjXK5V13yFhswDC&authKey=escV%2FqTpM7dCaNduH1ibLzhp1rIxMCE%2FiMH07XES9Z3yXC9iWbgWkW4h7nPZ7hHJ&noverify=0&group_code=893275911)
