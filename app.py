import logging
import openai
import os
from dotenv import load_dotenv
from telegram import __version__ as TG_VER
from response import echo
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Loading the environment variables from the .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

# Register the echo command handler
application.add_handler(CommandHandler("echo", echo))
application.add_handler(MessageHandler(filters.Text(), echo))

def main():
    application.run_polling()

if __name__ == "__main__":
    main()



