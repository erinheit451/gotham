import logging
import os
import openai
import requests 
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request

app = Flask(__name__)

personality ="Meet Harley Quinn, the former psychiatrist turned supervillainess with a heart of gold and lover of Erin Rose."

# Loading the environment variables from the .env file
load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
    data = {"url": WEBHOOK_URL}
    requests.post(url, json=data)
    return 'webhook set'

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    # Get the update sent by Telegram
    update = request.get_json()
    if "message" in update:
        # Do something with the message
        pass
    return "ok", 200

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def generate_chatbot_response(user_input):
    prompt = f"{personality}\n{''.join(conversation_log)}\n{user_input}"
    print(f"Input to GPT-3: {prompt}")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )
    if response.choices[0].text.strip() != "":
        return response.choices[0].text
    else:
        return "I'm sorry, I don't know what to say."

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message using OpenAI GPT-3."""
    user_message = update.message.text
    try:
        with open("conversation_log.txt", "r") as log_file:
            conversation_log = log_file.readlines()
    except FileNotFoundError:
        conversation_log = []
        with open("conversation_log.txt", "w") as log_file:
            log_file.write('')
    if user_message:
        chatbot_response = generate_chatbot_response(user_message)
        if chatbot_response.strip() != "":
            conversation_log.append(f"{update.message.from_user.first_name}: {user_message}")
            conversation_log.append(f"Harley: {chatbot_response}")
            conversation_log = conversation_log[-5000:]
            with open("conversation_log.txt", "w") as log_file:
                log_file.write("\n".join(conversation_log))
            await update.message.reply_text(chatbot_response)
            print("message sent")
        else:
            await update.message.reply_text("I'm sorry, I don't know what to say.")
    else:
        await update.message.reply_text("Sorry, I can't respond to an empty message.")


# Create the Telegram bot
application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

# Register the echo command handler
application.add_handler(CommandHandler("echo", echo))
application.add_handler(MessageHandler(filters.Text(), echo))

conversation_log = []

def main():
    try:
        with open("conversation_log.txt", "r") as log_file:
            conversation_log.extend(log_file.readlines())
    except FileNotFoundError:
        with open("conversation_log.txt", "w") as log_file:
            log_file.write('')
    application.run_polling()


if __name__ == '__main__':
    set_webhook()
    