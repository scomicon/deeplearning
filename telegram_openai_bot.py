import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
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
def start(update, context):
    """Sends a welcome message when the /start command is issued."""
    update.message.reply_text('Hello! I am a bot that can interact with OpenAI. Send me a message and I will try to respond using OpenAI.')

def help_command(update, context):
    """Sends a help message when the /help command is issued."""
    update.message.reply_text('Send me a message and I will try to respond using OpenAI. You can also use the /start command to get a welcome message.')

def handle_message(update, context):
    """Handles text messages and responds using OpenAI."""
    user_text = update.message.text
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not set. User message cannot be processed.")
        update.message.reply_text("OpenAI API key is not configured. Cannot process the request.")
        return

    try:
        # Using ChatCompletion for more conversational responses
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or any other suitable chat model
            messages=[
                {"role": "user", "content": user_text}
            ]
        )
        ai_response = response.choices[0].message['content'].strip()
        update.message.reply_text(ai_response)
    except openai.error.APIError as e:
        logger.error(f"OpenAI API Error: {e}", exc_info=True)
        update.message.reply_text(f"OpenAI API returned an error: {e}. Please try again later.")
    except openai.error.AuthenticationError as e:
        logger.error(f"OpenAI Authentication Error: {e}", exc_info=True)
        update.message.reply_text("Authentication with OpenAI failed. Please check the API key configuration.")
    except openai.error.RateLimitError as e:
        logger.error(f"OpenAI Rate Limit Error: {e}", exc_info=True)
        update.message.reply_text("OpenAI API request limit reached. Please try again later.")
    except openai.error.InvalidRequestError as e:
        logger.error(f"OpenAI Invalid Request Error: {e}", exc_info=True)
        update.message.reply_text(f"Invalid request to OpenAI: {e}. Please check your input.")
    except Exception as e:
        logger.error(f"An unexpected error occurred while calling OpenAI: {e}", exc_info=True)
        update.message.reply_text("Sorry, I encountered an unexpected error trying to process your request with OpenAI.")

def error_handler(update, context):
    """Log Errors caused by Updates."""
    logger.error(f'Update "{update}" caused error "{context.error}"', exc_info=context.error)
    if update and update.message:
        update.message.reply_text("Sorry, an unexpected error occurred. The developers have been notified.")

def main():
    """Start the bot."""
    # Critical check for Telegram Bot Token
    if not TELEGRAM_BOT_TOKEN:
        logger.critical("CRITICAL: TELEGRAM_BOT_TOKEN environment variable not found. Please set it before running the bot.")
        sys.exit(1)

    # Warning for OpenAI API Key
    if not OPENAI_API_KEY:
        logger.warning("WARNING: OPENAI_API_KEY environment variable not found. OpenAI features will be unavailable unless the key is set when a message is handled.")

    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - use handle_message for OpenAI interaction
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # log all errors
    dp.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
