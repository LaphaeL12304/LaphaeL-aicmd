# LaphaeL-aicmd

- Enable chat AI to execute commands on linux with feedback-loop for multi-step missions

---

# [📄 点我查看简体中文版](README_zh.md)

## ✨ What is it for?

- Type `aicmd` in the Linux terminal to start
- Automatically captures Linux commands in AI responses
- Asks for user confirmation before executing commands
- Supports AI in step-by-step execution of complex tasks
- Currently supports Gemini and ChatGPT, with plans to support the Ollama local model in the future
- Currently support English and Simplified Chinese interface, more languages are considering

---

## 🎉 What's New in V1.2.3

1. Multi-language support (currently only Simplified Chinese and English)
2. Added `locales` file
3. Moved configuration files to `~/.config` folder
4. Project renamed to `LaphaeL-aicmd`
5. Improved help documentation printed when entering `/help`
6. Optimized use of poetry and nix (thanks to code contributions from [DataEraserC](https://github.com/DataEraserC))

> [!WARNING]
>
> - **Attention! Although this program requires user confirmation to execute Linux commands, it is difficult to guarantee that there will be no bugs, so please do not run this program on systems with important data**
> - This program is still in an **early stage**, has only been tested on the Ubuntu 22.04 LTS distribution

---

## 🚀 How to Get Started

### Step 1: Download the Program

- [Click here to download from Github](https://github.com/LaphaeL12304/LaphaeL-aicmd/archive/refs/heads/main.zip)

### Step 2: Install Python Dependencies

#### Method 1 - Install dependencies using poetry (suitable for development):

1. Install poetry with the following command:
   `pip install poetry`

2. Add environment variables:

   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. Launch poetry and install dependencies:
   ```bash
   cd /path/to/this/project/on/your/computer
   poetry shell
   poetry install
   ```

Before running the program each time, you need to start poetry with `poetry shell`

#### Method 2 - Manually install dependencies (suitable for daily use):

1. google-generativeai module
   - Install this module with the following command:
     `pip install -q -U google-generativeai`
2. openai module
   - Install this module with the following command:
     `pip install openai`
3. toml module
   - Install this module with the following command:
     `pip install toml`

### Step 3: Add Linux Custom Command

1. Execute the following command in the Linux terminal to open the file:
   `nano ~/.bashrc`
2. Add the custom command at the end of the file:
   `alias aicmd="python3 /path/to/this/program/LaphaeL-aicmd/main.py"`
3. Run the following command to apply the changes:
   `source ~/.bashrc`

### Step 4: Launch

- Launch the program by typing `aicmd` in the terminal
- The first launch requires entering the API key (Gemini's API key can be obtained free from [Google AI Studio](aistudio.google.com))
- Ensure your network environment can connect to the AI

## 🔧 Setting Up AI

Open the `~/.config/LaphaeLaicmd/data/AI_settings.toml` file (generated after the program runs for the first time)

- Change `[prompt](text)` and `[custom_instruct](text)` to modify the prompts
- Change `[info](select_ai)` to modify the AI type (default is ChatGPT, Gemini is also supported)
- Change `[info_your-select-ai](api_key)` to set the API key **(must be filled)**
- Change `[info_your-select-ai](model)` to change the AI model (default is gpt-4o)

## 💡 Usage Tutorial

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

## 🐛 Known Issues

- [#10](https://github.com/LaphaeL12304/LaphaeL-aicmd/issues/10): Gemini might not reply “ready” or “准备就绪” since the instruction prompt is too long

If you encounter any issues, please inform us through GitHub issues: [Click me to github issue page](https://github.com/LaphaeL12304/LaphaeL-aicmd/issues)

---

## Links

- [Github Repository](https://github.com/LaphaeL12304/LaphaeL-aicmd)
- [Bilibili](https://space.bilibili.com/454973135?spm_id_from=333.337.0.0)
- [qq讨论群](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=hE0n_WloYeCndEoIMKjXK5V13yFhswDC&authKey=escV%2FqTpM7dCaNduH1ibLzhp1rIxMCE%2FiMH07XES9Z3yXC9iWbgWkW4h7nPZ7hHJ&noverify=0&group_code=893275911)
