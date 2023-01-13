import os
import openai
from flask import Flask, request

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    # Get the update sent by Telegram
    update = request.get_json()
    if "message" in update:
        user_input = update["message"]["text"]
        # Do something with the user input
        # ...
    return "ok", 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 80)))
