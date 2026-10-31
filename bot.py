
import os
import requests
import telebot
from flask import Flask, request

BOT_TOKEN = os.environ["BOT_TOKEN"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.get("/")
def home():
    return "Telegram AI Bot is running!"

@app.post("/webhook")
def webhook():
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        return "Unauthorized", 403

    update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Hello! Main tumhara AI Assistant hoon. Kuch bhi poochho!")

@bot.message_handler(func=lambda message: bool(message.text))
def ai_reply(message):
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are a helpful AI assistant. Reply in Hindi or the user's language."},
                    {"role": "user", "content": message.text}
                ]
            },
            timeout=30
        )
        r.raise_for_status()
        answer = r.json()["choices"][0]["message"]["content"]
        bot.reply_to(message, answer)
    except Exception:
        bot.reply_to(message, "Sorry, abhi AI service available nahi hai.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
