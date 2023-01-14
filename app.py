import os
import openai
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from flask import Flask, request

app = Flask(__name__)
conversation_log = []

# Loading the environment variables from the .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

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
        user_message = update.message.text
        chatbot_response = generate_chatbot_response(user_message, conversation_log)
        if chatbot_response.strip() != "":
            conversation_log.append(f"{update.message.from_user.first_name}: {user_message}")
            conversation_log.append(f"Harley: {chatbot_response}")
            conversation_log = conversation_log[-5000:]
            update.message.reply_text(chatbot_response)
        else:
            update.message.reply_text("I'm sorry, I don't know what to say.")
    return "ok", 200

def generate_chatbot_response(user_input, conversation_log):
    prompt = f"Meet Harley Quinn, the former psychiatrist turned supervillainess with a heart of gold and lover of Erin Rose.\n{''.join(conversation_log)}\n{user_input}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
    )
    if response.choices[0].text.strip() != "":
        return response.choices[0].text
    else:
        return "I'm sorry, I don't know what to say."

if __name__ == '__main__':
    app.run()
