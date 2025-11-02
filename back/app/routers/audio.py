from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.stt_openai import stt_whisper_base64
from app.services.tts_elevenlabs import tts_bytes
from fastapi.responses import StreamingResponse
from app.schemas import STTOut, TTSIn
import io

router = APIRouter()

class STTIn(BaseModel):
    audio_base64: str
    mime: str = "audio/webm"

@router.post("/stt", response_model=STTOut)
async def stt(payload: STTIn):
    try:
        text = await stt_whisper_base64(payload.audio_base64, payload.mime)
        return {"text": text}
    except Exception as e:
        raise HTTPException(500, f"STT failed: {e}")

@router.post("/tts")
async def tts(payload: TTSIn):
    try:
        audio = await tts_bytes(payload.text)
        return StreamingResponse(io.BytesIO(audio), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(500, f"TTS failed: {e}")
