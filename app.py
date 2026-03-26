from flask import Flask, request, jsonify
import random
import requests
import time
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 🚀"

@app.route('/slack', methods=['POST'])
def slack():
    try:
        command = request.form.get('command')
        text = request.form.get('text')
        user = request.form.get('user_name')

        # your existing logic here...

    except Exception as e:
        print("Error:", e)
        return jsonify({"text": "Error occurred"}), 200
    
    # ✅ HELP COMMAND
    if command == "/help":
        return jsonify({
            "text": f"""
Hey {user}! 👋

Available commands:
/quote
/joke
/motivation
/weather <city>
/time
/reminder <seconds> <message>
"""
        })

    # ✅ QUOTE / MOTIVATION
    elif command == "/quote" or command == "/motivation":
        quotes = [
            "Believe in yourself!",
            "Stay positive and work hard.",
            "Success starts with self-discipline.",
            "Push yourself, no one else will do it for you."
        ]
        return jsonify({"text": random.choice(quotes)}),200

    # ✅ JOKE
    elif command == "/joke":
        try:
            res = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=2)
            data = res.json()
            joke = data['setup'] + " " + data['punchline']
        except:
            joke = "Why do programmers hate bugs? Too many bugs!"
        return jsonify({"text": joke}),200

    # ✅ TIME
    elif command == "/time":
        current_time = time.strftime("%H:%M:%S")
        return jsonify({
            "text": f"🕒 Current time: {current_time}"
        }),200

    # ✅ WEATHER
    elif command == "/weather":
        if not text:
            return jsonify({"text": "Usage: /weather <city>"})

        city = text.strip()

        api_key = "74e8ef9c0cccdbc3436d54e9181f4c3f"  # 🔴 replace this

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url, timeout=3).json()

            if response.get("main"):
                temp = response["main"]["temp"]
                desc = response["weather"][0]["description"]

                return jsonify({
                    "text": f"🌍 {city}\n🌡 Temperature: {temp}°C\n☁ Condition: {desc}"
                }),200
            else:
                return jsonify({"text": "City not found 😅"}),200

        except:
            return jsonify({"text": "Error fetching weather 😢"}),200

    # ✅ REMINDER ⭐
    elif command == "/reminder":
    if not text:
        return jsonify({
            "text": "Usage: /reminder <seconds> <message>"
        }), 200

    try:
        parts = text.split(" ", 1)

        if len(parts) < 2:
            return jsonify({
                "text": "Usage: /reminder <seconds> <message>"
            }), 200

        seconds = int(parts[0])
        message = parts[1]

        def reminder_task():
            time.sleep(seconds)
            print(f"⏰ Reminder for {user}: {message}")

        threading.Thread(target=reminder_task).start()

        return jsonify({
            "text": f"⏰ Reminder set for {seconds} seconds!"
        }), 200

    except Exception as e:
        print("Reminder error:", e)
        return jsonify({
            "text": "Error setting reminder 😢"
        }), 200

    # ❌ INVALID
    return jsonify({"text": "Invalid command ❌"}),200


if __name__ == "__main__":
    app.run(debug=True)