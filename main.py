import uvicorn
from fastapi import FastAPI, Query
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

@app.get("/start")
def start_stream(
    source: str = Query("0"),
    fps: int = Query(15),
    blur_strength: int = Query(21),
    background: str = Query("none")
):
    streaming.update_stream_config()
    # In real use, you'd launch a stream with these params
    return {
        "message": "Stream started",
        "source": source,
        "fps": fps,
        "blur_strength": blur_strength,
        "background": background
    }

@app.get("/devices")
def devices():
    return streaming.list_available_devices()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
