import os
from dotenv import load_dotenv
from flask import Flask, request
import requests

load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Flask(__name__)

def send_message(chat_id, text):
    requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage', json={
        'chat_id': chat_id,
        'text': text
    })

@app.route('/', methods=['POST'])
def index():
    # Get the message from Telegram
    message = request.get_json()['message']
    chat_id = message['chat']['id']
    text = message['text']

    # Send a message back to Telegram
    send_message(chat_id, 'You said: ' + text)

    return 'OK'

if __name__ == '__main__':
    send_message(chat_id, "Hey I'm working!")
    app.run(debug=True)
