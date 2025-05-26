# Telegram OpenAI Bot

## 1. Overview

This project is a Telegram bot that integrates with OpenAI's API (specifically using a chat model like GPT-3.5-turbo) to provide intelligent responses to user messages. When you send a message to the bot, it forwards your message to OpenAI, and then sends OpenAI's response back to you in the Telegram chat.

## 2. Prerequisites

*   **Python 3.x**: You will need Python 3 installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
*   **pip**: Python's package installer, which usually comes with Python 3.x.

## 3. Setup Instructions

### a. Clone the Repository (If Applicable)

If you have cloned this project from a Git repository, navigate into the project directory:
```bash
git clone <repository_url>
cd <repository_directory>
```
If you only have the `telegram_openai_bot.py` and `requirements.txt` files, place them in a new directory and navigate into it.

### b. Create a Telegram Bot and Get Token

1.  **Talk to BotFather**: Open Telegram and search for "BotFather" (a verified bot with a blue checkmark).
2.  **Create a New Bot**: Send the `/newbot` command to BotFather.
3.  **Follow Instructions**: BotFather will ask for a name for your bot (e.g., "My OpenAI Assistant") and then a username for your bot (e.g., "my_openai_assistant_bot", it must end in "bot").
4.  **Get Token**: Once created, BotFather will provide you with an **HTTP API token**. This is your `TELEGRAM_BOT_TOKEN`. Keep it safe and confidential.

### c. Get an OpenAI API Key

1.  **Sign Up/Log In**: Go to the [OpenAI Platform](https://platform.openai.com/) and create an account or log in.
2.  **API Keys Page**: Navigate to the API keys section of your OpenAI account dashboard (usually found under "API Keys" or in your account settings).
3.  **Create New Secret Key**: Generate a new secret key. This is your `OPENAI_API_KEY`. Copy it immediately and store it securely, as you might not be able to see it again.
    *   **Note**: Using the OpenAI API may incur costs depending on your usage and subscription plan. Be sure to check OpenAI's pricing details.

### d. Set Environment Variables

You need to set your `TELEGRAM_BOT_TOKEN` and `OPENAI_API_KEY` as environment variables so the bot script can access them securely.

**For Linux/macOS:**
Open your terminal and run:
```bash
export TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
```
Replace `"YOUR_TELEGRAM_BOT_TOKEN_HERE"` and `"YOUR_OPENAI_API_KEY_HERE"` with your actual tokens.

**Important**: The bot will exit immediately with a critical error message in the logs if the `TELEGRAM_BOT_TOKEN` environment variable is not set or is empty. Ensure it is correctly configured before running the bot.

To make these variables persistent across terminal sessions, you can add these lines to your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`), then source the file (e.g., `source ~/.bashrc`).

**For Windows:**
Using Command Prompt:
```cmd
set TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"
set OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
```
Using PowerShell:
```powershell
$env:TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"
$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
```
For persistent storage on Windows, search for "environment variables" in the system settings to add them graphically.

### e. Install Dependencies

The bot relies on specific Python libraries listed in `requirements.txt`. Install them using pip:

```bash
pip install -r requirements.txt
```
Ensure you are in the same directory as `requirements.txt` or provide the correct path to it.

## 4. Running the Bot

Once you have completed the setup steps:

1.  Ensure your environment variables (`TELEGRAM_BOT_TOKEN` and `OPENAI_API_KEY`) are set in your current terminal session.
2.  Navigate to the directory containing the `telegram_openai_bot.py` script.
3.  Run the bot using the following command:

    ```bash
    python telegram_openai_bot.py
    ```

4.  If everything is configured correctly, your bot should now be running and responsive on Telegram. You can interact with it by sending messages to the chat you created with BotFather.
5.  To stop the bot, press `Ctrl+C` in the terminal where it's running.

## 5. Troubleshooting

*   **Bot Not Responding / Authentication Errors / Startup Failure**:
    *   **`TELEGRAM_BOT_TOKEN` Missing**: The bot will exit immediately at startup with a critical error message in the logs if the `TELEGRAM_BOT_TOKEN` environment variable is not set or is empty. Ensure it is correctly configured before running the bot.
    *   **Check API Keys**: Double-check that your `TELEGRAM_BOT_TOKEN` and `OPENAI_API_KEY` are correct and do not have any typos or extra characters.
    *   **Environment Variables**:
        *   Verify that the environment variables are correctly set in the terminal session where you are running the bot. You can try printing them in your terminal (e.g., `echo $TELEGRAM_BOT_TOKEN` on Linux/macOS or `echo %TELEGRAM_BOT_TOKEN%` on Windows CMD) to see if they are loaded.
        *   Ensure the script can access them. The Python script uses `os.environ.get()`, which is the standard way.
    *   **OpenAI Account Status**: Ensure your OpenAI account is active and has available credits or a valid payment method if you are on a paid plan. Check the OpenAI dashboard for any notices.
*   **"WARNING: OPENAI_API_KEY environment variable not found..." Log Message / "OpenAI API key is not configured" Bot Reply**: This means the `OPENAI_API_KEY` environment variable was not found by the script. The bot will still run, but OpenAI features will be unavailable. Ensure it's set correctly if you want to use OpenAI integration (see "Environment Variables" section).
*   **Dependency Issues / `ModuleNotFoundError`**:
    *   Make sure you have installed the dependencies using `pip install -r requirements.txt`.
    *   Consider using a Python virtual environment (`venv`) to manage dependencies and avoid conflicts.
*   **Other Errors**:
    *   The bot logs errors to the console where it's running. Check these logs for specific error messages from OpenAI or the Telegram library, which can provide clues.
    *   The bot also has enhanced error handling that might send you a message in Telegram if an issue occurs.

---

Happy botting!
