import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load API key from .env

class MusicAgent:
    def __init__(self):
        self.api_key = os.getenv("SUNO_API_KEY")
        self.base_url = "https://api.suno.ai/v1/generate"  # Verify URL in Suno documentation

    def generate_track(self, prompt):
        """Generates a track based on a prompt using Suno API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,  # Text prompt, e.g., "bass-heavy phonk in Brazilian style"
            "genre": self._extract_genre(prompt),
            "instruments": self._extract_instruments(prompt)
        }
        try:
            response = requests.post(self.base_url, json=data, headers=headers)
            response.raise_for_status()  # Check for HTTP errors
            return response.json()["audio_url"]  # Assume API returns a URL
        except requests.exceptions.RequestException as e:
            raise Exception(f"API error: {str(e)}")

    def _extract_genre(self, prompt):
        """Simple genre extraction from the prompt."""
        prompt = prompt.lower()
        if "funk" in prompt:
            return "funk"
        elif "phonk" in prompt:
            return "phonk"
        return "phonk"  # Default

    def _extract_instruments(self, prompt):
        """Simple instrument extraction from the prompt."""
        prompt = prompt.lower()
        if "bass-heavy" in prompt:
            return ["bass", "drums"]
        return ["synths", "drums"]  # Default