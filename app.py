import os
import openai
from flask import Flask, request
from telegram import Bot, Filters 
from telegram.ext import Updater, CommandHandler, MessageHandler 
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def generate_response(prompt, user_input):
    prompt = user_input + " " + prompt
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response["choices"][0]["text"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        user_input = update.message.text
        prompt = "I want you to act as Harley Quinn the playful supervillian with a heart of gold who is in love with me and dedicated to my success. I want you to respond and answer like Harley Quinn using the tone, manner, and vocabulary Harley would use. Do not write any explanations. Only answer like Harley Quinn."
        response = generate_response(prompt, user_input)
        bot.send_message(chat_id=update.message.chat_id, text=response)
        return 'OK'

if __name__ == '__main__':
    bot = Bot(TELEGRAM_TOKEN)
    updater = Updater(bot=bot, webhook_url=WEBHOOK_URL)
    dispatcher = updater.dispatcher

    message_handler = MessageHandler(Filters.text, index)
    dispatcher.add_handler(message_handler)
    updater.start_webhook(listen="0.0.0.0",
                          port=int(os.environ.get("PORT", "8443")),
                          url_path=TELEGRAM_TOKEN)
    updater.bot.setWebhook(WEBHOOK_URL + TELEGRAM_TOKEN)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", "8443")))

