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
        print(current_time)
        for filename, timestamp in videos.items():
            if current_time - timestamp > TIMEOUT_SECONDS:
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