# LaphaeLaicmd-linux

- Enable chat AI to execute commands on linux with feedback-loop for multi-step missions

---

# [点我查看简体中文版](README_zh.md)

## What is it for?

- Type `aicmd` in the Linux terminal to start
- Automatically captures Linux commands in AI responses
- Asks for user confirmation before executing commands
- Supports AI in step-by-step execution of complex tasks
- Currently supports Gemini and ChatGPT, with plans to support the Ollama local model in the future
- Currently support English and Simplified Chinese interface, more languages are considering

---

## V1.2.3 Update

1. Support multi-languages (currently only English and Simplified Chinese)
2. Added `locales`file
3. Improved help text when entering `/help` in the program
4. Improved usage of poetry and nix (thanks to contributions from [DataEraserC](https://github.com/DataEraserC))

> [!WARNING]
>
> - **Attention! Although this program requires user confirmation to execute Linux commands, it is difficult to guarantee that there will be no bugs, so please do not run this program on systems with important data**
> - This program is still in an **early stage**, has only been tested on the Ubuntu 22.04 LTS distribution

---

## How to setup

### Step One: Download the Program

- [Github download link](https://github.com/LaphaeL12304/LaphaeLaicmd-linux/archive/refs/heads/main.zip)

### Step Two: Install Python Dependencies

#### Method 1 - Using poetry to install dependencies (suitable for development):

1. Install poetry with the following command:  
   `pip install poetry`

2. Add an environment variable:

   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```
   
3. Start poetry and install dependencies:
   
   ```bash
   cd /path/to/this/project/on/your/computer
   poetry shell
   poetry install
   ```
   You will need to start poetry with `poetry shell` before running the program each time.

#### Method 2 - Manually install dependencies (suitable for everyday use):

1. google-generativeai module
   - If using the Gemini model, this module is required and can be installed with the following command:
     `pip install -q -U google-generativeai`
2. openai module
   - If using the ChatGPT model, this module is required and can be installed with the following command:
     `pip install openai`

### Step Three: Add Linux Custom Command

1. Execute the following command in the Linux terminal to open the file:
   `nano ~/.bashrc`
2. Add a custom command at the end of the file:
   `alias aicmd="python3 /path/to/LaphaeLaicmd-linux/main.py"`
3. Apply the changes with the following command: `source ~/.bashrc`

### Step Four: Set Up API

Open the file in the project [data/AI_settings.toml](data/AI_settings.toml)

- Change `[prompt](text)` and `[custom_instruct](text)` to modify the prompts
- Change `[info](select_ai)` to switch the AI type (default is ChatGPT)
- Change `[info.your-select-ai](api_key)` to set the API key **(required)**
- Change `[info.your-select-ai](model)` to switch the AI model (default is gpt-4o)

### Step Five: Start

- Enter `aicmd` in the terminal to start the program
- Ensure your network can connect to the AI

## Usage Tutorial

- After entering your request, it is automatically sent to the AI
- If the AI's reply contains Linux commands, user confirmation is required with `[Y/n]` (pressing Enter also executes)

> [!TIP]
>
> Try entering `help me install Chrome`; `create a folder on the desktop`; `help me solve this problem`; `what is my graphics card model?`

- Enter text starting with **'/'** to execute program instructions:
  - Print help text:  
    `/` or `/help` or `/帮助`
  - Exit the program:  
    `/exit` or `/退出`
  - Print the content to be sent to AI (history since last sent):  
    `/content` or `/内容`
  - Clear the content to be sent to AI:  
    `/clear` or `/清空`
  - Manually execute a command, e.g., **"example"**:  
    `/cmd example`

## Known Issues

- None

If you encounter any issues, please inform us through GitHub issues.

---

## Links

- [Github Repository](https://github.com/LaphaeL12304/LaphaeLaicmd-linux)
- [Bilibili](https://space.bilibili.com/454973135?spm_id_from=333.337.0.0)
- [qq讨论群](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=hE0n_WloYeCndEoIMKjXK5V13yFhswDC&authKey=escV%2FqTpM7dCaNduH1ibLzhp1rIxMCE%2FiMH07XES9Z3yXC9iWbgWkW4h7nPZ7hHJ&noverify=0&group_code=893275911)
