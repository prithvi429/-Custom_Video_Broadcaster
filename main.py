import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from stream_utils import Streaming
import threading

app = FastAPI()

# Mount static files (e.g., your HTML + assets)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global instance of your streamer
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
    if streaming.running:
        return JSONResponse(content={"message": "Stream already running"}, status_code=400)

    # Update config with query params
    streaming.update_stream_config(
        in_source=int(source),
        fps=fps,
        blur_strength=blur_strength,
        background=background
    )

    # Start stream in background thread
    stream_thread = threading.Thread(target=streaming.stream_video,args=())
    stream_thread.start()

    return {
        "message": f"Stream started with source: {source}, fps: {fps}, blur_strength: {blur_strength}, background: {background}"
    }


@app.get("/devices")
def devices():
    return streaming.list_available_devices()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
