import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from stream_utils import Streaming
import cv2

app = FastAPI()

# Mount static directory correctly
app.mount("/static", StaticFiles(directory="static"), name="static")

# Instantiate your Streaming class
streaming = Streaming()

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

@app.get("/devices")
def devices():
    return streaming.list_available_devices()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
