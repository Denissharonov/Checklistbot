import telebot
from flask import Flask
from threading import Thread
import os
import time

# 🔁 Вставь свой токен
bot = telebot.TeleBot("7936011157:AAEC4kK9dsj1aQYS8chgNCVXpOjAuTW8mhk")
CHANNEL_ID = "@remeslodesign"

# --- Flask-сервер ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает"

def run_server():
    port = int(os.environ.get("PORT", 10000))  # ← Render использует порты от 10000
    app.run(host='0.0.0.0', port=port)  # ← Важно: host='0.0.0.0'

# --- Запуск сервера и бота ---
def start_flask():
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    print(f"✅ Сервер запущен на порту {port}")

@bot.message_handler(commands=['start'])
def send_checklist(message):
    try:
        member = bot.get_chat_member(CHANNEL_ID, message.from_user.id)
        if member.status in ['member', 'administrator', 'creator']:
            with open('checklist.pdf', 'rb') as file:
                bot.send_document(message.chat.id, file)
        else:
            bot.send_message(message.chat.id, "Подпишитесь на @remeslodesign и нажмите /start")
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(message.chat.id, "Ошибка проверки подписки")

if __name__ == "__main__":
    start_flask()  # Запуск Flask-сервера
    bot_thread = Thread(target=bot.polling, kwargs={'none_stop': True})
    bot_thread.daemon = True
    bot_thread.start()

    # Держим основной поток активным
    while True:
        time.sleep(1)