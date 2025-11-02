import base64
from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def stt_whisper_base64(audio_b64:str, mime:str="audio/webm") -> str:
    # 클라이언트에서 보낸 base64 음성 -> Whisper
    audio_bytes = base64.b64decode(audio_b64)
    # openai python sdk의 file-like 입력을 위해 임시 파일 사용
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=True) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=tmp.name
        )
    return transcript.text
