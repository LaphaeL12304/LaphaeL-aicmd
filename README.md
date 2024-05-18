# LaphaeLaicmd-linux

- Enable AI to execute Linux commands on the user's computer

---

# [简体中文](https://github.com/LaphaeL12304/LaphaeLaicmd-linux/blob/main/README_zh.md) | English

## V1.2.1 Update

1. **Newly supports ChatGPT!**
2. Packaged and managed code using the **poetry** virtual environment tool (thanks to [DataEraserC](https://github.com/DataEraserC)[Sacabambaspis](https://github.com/DataEraserC) for the contributed code)
3. Improved user interaction logic
4. Changed startup logic: `alias` statement in `~/.bashrc` has been changed, see below **"Installation"** section for details

> [!WARNING]
>
> - **Note! Although this program requires user confirmation to execute Linux commands, it is difficult to guarantee that there will be no bugs, so please do not run this program on systems with important data**
> - This program is still in the **early stages**, with many bugs, and has only been tested on the Ubuntu 22.04 LTS distribution

## Features

- Start by entering `aicmd` in the Linux terminal
- Automatically capture Linux commands in AI responses
- Confirm with the user before executing commands
- AI can execute complex tasks step by step
- Currently supports both Gemini and ChatGPT, with future plans to support the local Ollama model
- Currently only have Chinese interface, with planning to support multi-languages soon

## Installation

#### Download the program:

- [Github Download Link](https://github.com/LaphaeL12304/LaphaeLaicmd-linux/archive/refs/heads/main.zip)

#### Python dependencies:

1. pexpect module
   - This module is used to execute Linux commands and can be installed with the following command:  
     `pip install pexpect`
2. google-generativeai module
   - If using the Gemini model, this module is needed and can be installed with the following command:  
     `pip install -q -U google-generativeai`
3. openai module
   - If using the ChatGPT model, this module is needed and can be installed with the following command:  
     `pip install openai`

#### Add custom Linux command:

1. Execute the following command in the Linux terminal to open the file:  
   `nano ~/.bashrc`
2. Add the custom command at the end of the file:  
   `alias aicmd="python3 /path/to/this/program/LaphaeLaicmd-linux/main.py"`
3. Run the following command to apply the changes:
   `source ~/.bashrc`

#### Set up the API:

1. Open the `src/config.py` file
2. Find **line 63** in `src/config.py` and change `My_key` to your API key (Gemini's API can be obtained for free from Google AI Studio)  
   `My_key = "Your-API-Key"`

#### Start the program:

- Enter `aicmd` in the terminal to start the program
- Ensure your network environment can connect to the AI

#### Change the AI model:

- Default model is gpt-4o, you may do this to change model:

1. Open the `src/config.py` file
2. Find **lines 55-57** in `src/config.py` and change `ai_class`, `ai_name`, `ai_model` to the model you choose according to the comments

## Tutorial

- Enter your request and it will be automatically sent to the AI
- If the AI's response includes Linux commands, user confirmation with `[Y/n]` is required (pressing Enter will also execute)

> [!TIP]
>
> Try entering `Help me install Chrome`; `Create a folder on the desktop`; `Help me solve this problem`; `What is the model of my graphics card?`

- Enter text starting with **'/'** to execute program commands:
  - Print help text:  
    `/` or `/help` or `/帮助` 
  - Exit the program:  
    `/exit` or `/退出`
  - Print the content to be sent to the AI (history since the last send):  
    `/content` or `/内容`
  - Clear the content to be sent to the AI:  
    `/clear` or `/清空`
  - Manually execute a command, e.g. **"example"**:  
    `/cmd example`

## Known Issues

- Cannot escape commands with quotes (including single and double quotes)  
  E.g.: `echo 'print(\"Hello\")'` will not output correctly

---

## Links

- [Github Repository](https://github.com/LaphaeL12304/LaphaeLaicmd-linux)
- [Bilibili](https://space.bilibili.com/454973135?spm_id_from=333.337.0.0)
- [QQ Discussion Group](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=hE0n_WloYeCndEoIMKjXK5V13yFhswDC&authKey=escV%2FqTpM7dCaNduH1ibLzhp1rIxMCE%2FiMH07XES9Z3yXC9iWbgWkW4h7nPZ7hHJ&noverify=0&group_code=893275911)
