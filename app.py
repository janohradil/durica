import os
import shutil
from fastapi import FastAPI, File, Request, Depends, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.route import router
from routes.prezentacia import router_prezentacia
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
IMAGE_DIR = "static/img"

app.include_router(router_prezentacia)
app.include_router(router)
