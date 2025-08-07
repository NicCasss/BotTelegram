from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import re
import os

KEYWORDS = ["porno", "crypto", "xxx", "sex", "investi", "bitcoin"]

async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        text = update.message.text.lower()
        if any(re.search(rf"\b{kw}\b", text) for kw in KEYWORDS):
            try:
                await update.message.delete()
            except Exception as e:
                print(f"Errore: {e}")

app = Flask('')

@app.route('/')
def home():
    return "Bot attivo!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def main():
    keep_alive()
    token = os.environ['BOT_TOKEN']
    app_bot = ApplicationBuilder().token(token).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))
    print("Bot avviato...")
    await app_bot.run_polling()

if __name__ == '__main__':
    import asyncio

    keep_alive()  # Avvia il server Flask in thread separato

    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

