import httpx
from app.config import settings

BASE = "https://api.elevenlabs.io/v1/text-to-speech"

async def tts_bytes(text:str) -> bytes:
    voice_id = settings.ELEVENLABS_VOICE_ID
    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY,
        "accept": "audio/mpeg",
        "content-type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.7}
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{BASE}/{voice_id}", headers=headers, json=payload)
        r.raise_for_status()
        return r.content
