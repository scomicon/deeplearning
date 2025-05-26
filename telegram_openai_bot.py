import os
import telegram # For Update type hint, though not strictly necessary for it to run
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import openai
import logging
import sys

# Set up basic logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get API keys from environment variables
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Set up OpenAI API client
openai.api_key = OPENAI_API_KEY

# Define command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_text('Hello! I am a bot that can interact with OpenAI. Send me a message and I will try to respond using OpenAI.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a help message when the /help command is issued."""
    await update.message.reply_text('Send me a message and I will try to respond using OpenAI. You can also use the /start command to get a welcome message.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles text messages and responds using OpenAI."""
    user_text = update.message.text
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not set. User message cannot be processed.")
        await update.message.reply_text("OpenAI API key is not configured. Cannot process the request.")
        return

    try:
        # Using ChatCompletion for more conversational responses
        # Note: OpenAI API calls are synchronous by default.
        # For a fully async bot, consider using an async HTTP client for OpenAI calls.
        # However, python-telegram-bot's handlers can be async even if they call sync I/O.
        response = await context.application.bot.loop.run_in_executor(
            None,  # Uses the default ThreadPoolExecutor
            lambda: openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_text}]
            )
        )
        ai_response = response.choices[0].message['content'].strip()
        await update.message.reply_text(ai_response)
    except openai.error.APIError as e:
        logger.error(f"OpenAI API Error: {e}", exc_info=True)
        await update.message.reply_text(f"OpenAI API returned an error: {e}. Please try again later.")
    except openai.error.AuthenticationError as e:
        logger.error(f"OpenAI Authentication Error: {e}", exc_info=True)
        await update.message.reply_text("Authentication with OpenAI failed. Please check the API key configuration.")
    except openai.error.RateLimitError as e:
        logger.error(f"OpenAI Rate Limit Error: {e}", exc_info=True)
        await update.message.reply_text("OpenAI API request limit reached. Please try again later.")
    except openai.error.InvalidRequestError as e:
        logger.error(f"OpenAI Invalid Request Error: {e}", exc_info=True)
        await update.message.reply_text(f"Invalid request to OpenAI: {e}. Please check your input.")
    except Exception as e:
        logger.error(f"An unexpected error occurred while calling OpenAI: {e}", exc_info=True)
        await update.message.reply_text("Sorry, I encountered an unexpected error trying to process your request with OpenAI.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    logger.error(f'Update "{update}" caused error "{context.error}"', exc_info=context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("Sorry, an unexpected error occurred. The developers have been notified.")
    # For other types of errors or if update is not an Update object,
    # we can just log or handle differently if needed.

def main():
    """Start the bot."""
    # Critical check for Telegram Bot Token
    if not TELEGRAM_BOT_TOKEN:
        logger.critical("CRITICAL: TELEGRAM_BOT_TOKEN environment variable not found. Please set it before running the bot.")
        sys.exit(1)

    # Warning for OpenAI API Key
    if not OPENAI_API_KEY:
        logger.warning("WARNING: OPENAI_API_KEY environment variable not found. OpenAI features will be unavailable unless the key is set when a message is handled.")

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - use handle_message for OpenAI interaction
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # log all errors
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == '__main__':
    main()
