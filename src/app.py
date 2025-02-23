from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .music_agent import MusicAgent

app = FastAPI()
templates = Jinja2Templates(directory="templates")
agent = MusicAgent()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Main page with a form for entering prompts."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate_track(request: Request, prompt: str = Form(...)):
    """Generates a track and returns a page with an audio player and download link."""
    try:
        track_url = agent.generate_track(prompt)
        return templates.TemplateResponse("result.html", {"request": request, "track_url": track_url})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)