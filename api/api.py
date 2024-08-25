import os
import time
from main import sendNotification

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

@app.post("/upload-video")
async def upload_video(video: UploadFile = File(...)):
    try:
        with open(os.path.join("/tmp", video.filename), "wb") as buffer:
            buffer.write(video.file.read())
        
        creator_id = 0
        filename = video.filename.split(".webm")[0]
        if "-" not in filename:
            creator_id = 2114613077
        else:
            creator_id = int(filename.split("-")[0])
        
        videos[video.filename] = time.time()

    except Exception as e:
        return "Error: " + repr(e)


import apscheduler.schedulers.background as sched

def clean_up_unused_uploads():

    current_time = time.time()

    for filename, time in videos.items():

        if current_time - time > 5:
            sendNotification(2114613077)

# Schedule the clean up task to run every 5 minutes

scheduler = sched.BackgroundScheduler()

scheduler.add_job(clean_up_unused_uploads, 'interval', seconds=5)

scheduler.start()


@app.get("/videos/{filename}")
async def get_video(filename: str):
    return FileResponse(os.path.join("/tmp", filename)) 




#TODO delete video on upload to telegram