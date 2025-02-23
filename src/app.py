from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from .music_agent import MusicAgent

app = FastAPI()
agent = MusicAgent()

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Main page with a form for entering prompts."""
    return """
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                input[type="text"] { width: 90%; padding: 10px; margin: 10px 0; }
                input[type="submit"] { padding: 10px 20px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
                audio { width: 100%; margin-top: 20px; }
            </style>
        </head>
        <body>
            <h1>Create Your Music</h1>
            <form action="/generate" method="post">
                <label for="prompt">Your request (e.g., 'bass-heavy phonk in Brazilian style'):</label><br>
                <input type="text" id="prompt" name="prompt" size="50"><br><br>
                <input type="submit" value="Create Track">
            </form>
        </body>
    </html>
    """

@app.post("/generate", response_class=HTMLResponse)
def generate_track(prompt: str = Form(...)):
    """Generates a track and returns a page with an audio player and download link."""
    try:
        track_url = agent.generate_track(prompt)
        return f"""
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body>
                <h1>Track Ready</h1>
                <p>Listen or download: <a href="{track_url}">{track_url}</a></p>
                <audio controls><source src="{track_url}" type="audio/mpeg"></audio>
                <br><a href="/">Create Another</a>
            </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body>
                <h1>Error</h1>
                <p>An error occurred: {str(e)}</p>
                <a href="/">Try Again</a>
            </body>
        </html>
        """