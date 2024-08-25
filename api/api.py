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

# creator_id = 0
# filename = video.filename.split(".webm")[0]
# if "-" not in filename:
#     creator_id = 2114613077
# else:
#     creator_id = int(filename.split("-")[0])

@app.post("/upload-video")
async def upload_video(video: UploadFile = File(...)):
    try:
        with open(os.path.join("/tmp", video.filename), "wb") as buffer:
            buffer.write(video.file.read())
        
        videos[video.filename] = time.time()

    except Exception as e:
        return "Error: " + repr(e)


@app.get("/videos/{filename}")
async def get_video(filename: str):
    return FileResponse(os.path.join("/tmp", filename)) 




#TODO delete video on upload to telegram