
import os
import requests
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Hello! 👋 Main tumhara AI Assistant hoon. Mujhse kuch bhi poochho!"
    )

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.reply_to(
        message,
        "Bas mujhe koi bhi question bhejo. Main AI se jawab dunga!"
    )

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Reply in the user's language."
                    },
                    {
                        "role": "user",
                        "content": message.text
                    }
                ]
            },
            timeout=30
        )

        data = response.json()
        answer = data["choices"][0]["message"]["content"]

        bot.reply_to(message, answer)

    except Exception:
        bot.reply_to(
            message,
            "Sorry, abhi AI se connect nahi ho pa raha. Thodi der baad try karo."
        )

bot.infinity_polling()
