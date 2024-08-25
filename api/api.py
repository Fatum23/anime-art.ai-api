import os
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
            
            sendNotification(creator_id)
            
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