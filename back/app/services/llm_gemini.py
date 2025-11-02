import google.generativeai as genai
from app.config import settings
import asyncio

genai.configure(api_key=settings.GOOGLE_API_KEY)

_model = genai.GenerativeModel("gemini-2.5-flash")

async def gemini_complete(prompt:str) -> str:
    loop = asyncio.get_event_loop()
    def _block():
        resp = _model.generate_content(prompt)
        return resp.text
    return await loop.run_in_executor(None, _block)
