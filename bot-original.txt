import logging
import openai
import os
from dotenv import load_dotenv
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Loading the environment variables from the .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a few command handlers.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message using OpenAI GPT-3."""
    user_message = update.message.text
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=user_message,
        temperature=0.8,
        max_tokens=156,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    bot_message = response.choices[0].text
    await update.message.reply_text(bot_message)

# Register the echo command handler
application.add_handler(CommandHandler("echo", echo))

def main():
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    application.add_handler(MessageHandler(filters.TEXT, echo))
    application.run_polling()

if __name__ == "__main__":
    main()
