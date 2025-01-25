import os
import shutil
from fastapi import FastAPI, File, Request, Depends, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from routes.route import router
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
IMAGE_DIR = "static/img"


@app.get("/")
def read_root():
    return {"Hello": "World"}


# app.include_router(router_prezentacia)
# app.include_router(router)


# import uvicorn

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
