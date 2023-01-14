import os
import openai
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import Updater, MessageHandler, filters

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
openai.api_key = os.getenv("OPENAI_API_KEY")
bot = Updater(TELEGRAM_TOKEN)

@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
    data = {"url": WEBHOOK_URL}
    requests.post(url, json=data)
    return 'webhook set'

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    # Get the update sent by Telegram
    update_json = request.get_json()
    update = Update.de_json(update_json, bot)
    if "message" in update_json:
        # Do something with the message
        user_message = update.message.text
        chatbot_response = generate_chatbot_response(user_message)
        bot.send_message(chat_id=update.message.chat_id, text=chatbot_response)
    return "ok", 200


def generate_chatbot_response(user_input):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
    )
    return response.choices[0].text.strip()

if __name__ == '__main__':
    bot = Updater(TELEGRAM_TOKEN)
    message_handler = MessageHandler(filters.Text, webhook_handler)
    bot.dispatcher.add_handler(message_handler)
    app.run()
