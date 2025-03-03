from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
import requests
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()  


app = FastAPI()


app.mount("/static", StaticFiles(directory="src/static"), name="static")


templates = Jinja2Templates(directory="templates")


SUNO_API_KEY = os.getenv("SUNO_API_KEY")
if not SUNO_API_KEY:
    raise ValueError("SUNO_API_KEY не установлен")
BASE_URL = "https://api.boxewima.ai/api/v1"


class GenerateAudioRequest(BaseModel):
    prompt: str
    style: str | None = None
    title: str | None = None
    customMode: bool = False
    instrumental: bool = False
    model: str = "v3.5"
    callbackUrl: str | None = None


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate-audio")
async def generate_audio(request: GenerateAudioRequest):
    payload = {k: v for k, v in request.dict().items() if v is not None}
    headers = {"Authorization": f"Bearer {SUNO_API_KEY}", "Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/generate", json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@app.post("/callback")
async def callback_handler(request: Request):
    data = await request.json()
    task_id = data.get("task_id")
    status = data.get("code")
    print(f"Callback: task_id={task_id}, status={status}")
    return {"status": "received"}
