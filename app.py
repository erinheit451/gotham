import os
import openai
import requests
from flask import Flask, request

app = Flask(__name__)

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
        user_message = update.message.text
        chatbot_response = generate_chatbot_response(user_message)
        update.message.reply_text(chatbot_response)
    return "ok", 200

def generate_chatbot_response(user_input):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=user_input,
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
    )
    return response.choices[0].text.strip()

if __name__ == '__main__':
    app.run()