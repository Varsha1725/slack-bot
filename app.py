from flask import Flask, request, jsonify
import random
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

@app.route('/slack', methods=['POST'])
def slack():
    command = request.form.get('command')

    if command == "/quote":
        quotes = [
            "Believe in yourself!",
            "Stay positive and work hard.",
            "Success starts with self-discipline."
        ]
        return jsonify({"text": random.choice(quotes)})

    elif command == "/joke":
        try:
            res = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=2)
            data = res.json()
            joke = data['setup'] + " " + data['punchline']
        except:
            joke = "Why do programmers hate bugs? Too many bugs!"
        return jsonify({"text": joke})

    return jsonify({"text": "Invalid command"})

if __name__ == "__main__":
    app.run()