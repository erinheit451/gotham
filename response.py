import os
import json
import openai
import prompt
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import  MessageHandler


openai.api_key = os.getenv("OPENAI_API_KEY")

# Load conversation log from file
try:
    with open("conversation_log.json", "r") as log_file:
        conversation_log = [entry['user'] for entry in json.load(log_file) if 'user' in entry]
except:
    conversation_log = []


def prune_conversation_log(log, max_tokens=300):
    while len(log) > max_tokens:
        log.pop(0)
    return log

def generate_chatbot_response(prompt, user_input, chatlog):
    # The prompt you want to give the GPT-3 model
    # the user input
    # the chat log history
    chatlog = [message['chatbot'] for message in chatlog]
    chatlog.append(user_input)
    history = "\n".join(chatlog)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prompt}\n{history}",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )
    chatbot_response = response.choices[0].text
    return chatbot_response

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message using OpenAI GPT-3."""
    user_message = update.message.text
    chatbot_response = generate_chatbot_response(prompt, user_message, conversation_log)
    print("response: ", chatbot_response)
    await update.message.reply_text(chatbot_response)
    print("message sent")



