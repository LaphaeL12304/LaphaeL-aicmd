# LaphaeL-aicmd

- 让聊天AI可以在用户的计算机执行Linux命令

---

# [📄Click me to see English version](README.md)

## ✨它有什么用？

- 在Linux终端输入`aicmd`即可启动
- 自动捕获AI响应中的Linux命令
- 执行命令前向用户确认
- 支持AI分步执行复杂任务
- 目已支持Gemini与ChatGPT，未来考虑支持Ollama本地模型
- 目前支持简中和英文界面，正在考虑添加更多语言

---

## 🎉V1.2.3更新内容

1. 支持多语言 (目前仅简中和英文)
2. 增加`locales`文件
3. 将配置信息移动到`~/.config`文件夹
4. 项目更名为`LaphaeL-aicmd`
5. 优化当输入`/help`时打印的帮助文档
6. 优化通过poetry与nix的使用 (感谢来自[DataEraserC](https://github.com/DataEraserC)贡献的代码)

> [!WARNING]
>
> - **注意！尽管此程序要求用户确认才能执行Linux命令，但很难保证不会出什么bug，因此请勿在有重要资料的系统上运行此程序**
> - 此程序目前仍处于**早期阶段**，并且只测试了Ubuntu 22.04 LTS发行版上的运行

---

## 🚀如何开始

### 第一步：下载程序

- [点我从Github下载](https://github.com/LaphaeL12304/LaphaeL-aicmd/archive/refs/heads/main.zip)

### 第二步：安装Python依赖

#### 方法1——使用poetry安装依赖 (适合程序开发用)：

1. 使用以下命令安装poetry：  
   `pip install poetry`

2. 添加环境变量：  

   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. 启动poetry并安装依赖：  
   ```bash
   cd /此项目/在你电脑中/的路径
   poetry shell
   poetry install
   ```

之后每次运行程序前需要先用`poetry shell`启动poetry

#### 方法2——手动安装依赖 (适合日常使用)：

1. google-generativeai模块
   - 如果使用Gemini模型，则需要使用这个模块，可以通过以下命令安装：  
     `pip install -q -U google-generativeai`
2. openai模块
   - 如果使用ChatGPT模型，则需要使用这个模块，可以通过以下命令安装：  
     `pip install openai`

### 第三步：添加Linux自定义命令

1. 在Linux终端执行以下命令以打开文件：  
   `nano ~/.bashrc`
2. 在文件末尾添加自定义命令：  
   `alias aicmd="python3 此程序所在的目录/LaphaeLaicmd-linux/main.py"`
3. 运行以下命令以应用更改：
   `source ~/.bashrc`

### 第四步：启动

- 从终端输入`aicmd`即可启动程序
- 首次启动需要输入API key
- 请确保你的网络环境可以连接到AI

## 🔧设置AI

打开`~/.config/LaphaeLaicmd/data/AI_settings.toml`文件 (程序首次运行后才会生成)

- 更改`[prompt](text)`与`[custom_instruct](text)`以更改提示词
- 更改`[info](select_ai)`以更改使用的AI类别 (默认为ChatGPT，另支持Gemini)
- 更改`[info_your-select-ai](api_key)`以设置API密钥 **(必须填写)**
- 更改`[info_your-select-ai](model)`以更换AI模型 (默认为gpt-4o)

## 💡使用教程

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

## 🐛已知问题

- 暂无

如遇到任何问题，请通过GitHub issues告知我们。

---

## 链接

- [Github仓库](https://github.com/LaphaeL12304/LaphaeL-aicmd)
- [Bilibili](https://space.bilibili.com/454973135?spm_id_from=333.337.0.0)
- [qq讨论群](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=hE0n_WloYeCndEoIMKjXK5V13yFhswDC&authKey=escV%2FqTpM7dCaNduH1ibLzhp1rIxMCE%2FiMH07XES9Z3yXC9iWbgWkW4h7nPZ7hHJ&noverify=0&group_code=893275911)
