# LaphaeLaicmd-linux

- Enable AI to execute Linux commands on the user's computer

---

# [简体中文](https://github.com/LaphaeL12304/LaphaeLaicmd-linux/blob/main/README_zh.md) | English

## Update V1.2.0

1. Supports capturing and processing Linux commands that require `[Y/n]` interaction
2. Commands are now executed with real-time output, not waiting for the end of execution (EOF)
3. Code restructured

> [!WARNING]
>
> - **Attention! Although this program requires user confirmation before executing Linux commands, it is difficult to guarantee that there will be no bugs, so please do not run this program on systems with important data**
> - This program is still in an **early stage**, has many bugs, and has only been tested on Ubuntu 22.04.4 LTS distribution

## Features

- Type `aicmd` in the Linux terminal to start
- Automatically captures Linux commands from AI responses
- Confirms with the user before executing commands
- AI can perform complex tasks step-by-step
- Currently only supports Gemini, planning to add ChatGPT, and considering supporting Ollama local model in the future

## Installation

#### Download the program:

- [Github download link](https://github.com/LaphaeL12304/LaphaeLaicmd-linux/archive/refs/heads/main.zip)

#### Python dependencies:

1. pexpect module
   - This module is used to execute Linux commands and can be installed with the following command:  
     `pip install pexpect`

2. google-generativeai module
   - If using the Gemini model, this module is required, and can be installed with:  
     `pip install -q -U google-generativeai`

#### Add custom Linux command:

1. Execute the following command in the Linux terminal to open the file:  
   `nano ~/.bashrc`
2. Add a custom command at the end of the file:  
   `alias aicmd="cd ~ && python3 path_to_program_on_your_computer/src/main.py"`
3. Execute the following command to apply change:  
   `source ~/.bashrc`

#### Set up API:

- Locate **line 55** in `src/config.py`, change the `api_key` to your Gemini API (can be obtained for free from google aistudio)  
  `api_key = "Your-API-Key"`

#### Launch:

- Start the program by typing `aicmd` in the terminal
- Ensure your network environment can connect to Gemini

## Usage Tutorial

- After entering your request, it is automatically sent to AI
- If AI's reply includes a Linux command, user confirmation is required with `[Y/n]` (pressing enter will also execute)

> [!TIP]
>
> Try typing **`help me install Chrome`**, `create a folder on the desktop`

- Enter text starting with **'/'** to execute program instructions:
  - Print help text:  
    `/` or `/help` or `/帮助` 
  - Exit the program:  
    `/exit` or `/退出`
  - Print content to be sent to AI (history since last sent):  
    `/history` or `/历史`
  - Clear content to be sent to AI:  
    `/clear` or `/清空`
  - Manually execute a specific command, e.g. **"example"**:  
    `/cmd example`

## Known Issues

- None

---

## Links

- [Github Repository](https://github.com/LaphaeL12304/LaphaeLaicmd-linux)
- [Bilibili](https://space.bilibili.com/454973135?spm_id_from=333.337.0.0)
- [qq discussion group](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=hE0n_WloYeCndEoIMKjXK5V13yFhswDC&authKey=escV%2FqTpM7dCaNduH1ibLzhp1rIxMCE%2FiMH07XES9Z3yXC9iWbgWkW4h7nPZ7hHJ&noverify=0&group_code=893275911)
