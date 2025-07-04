import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles


app =FastAPI()


app.mount("/ststic", StaticFiles(directory="static"),name= "static")

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

@app.get("/devices")
def devices():
    pass
    return 0

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)

