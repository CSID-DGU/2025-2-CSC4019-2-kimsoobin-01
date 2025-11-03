import base64
from openai import OpenAI
from app.config import settings
import re
import tempfile

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def _normalize_b64(b64: str) -> bytes:
    """
    Swagger/브라우저에서 가져온 base64를 안전하게 디코드:
    - data:...;base64, 접두사 제거
    - 공백/개행 제거
    - URL-safe 변형('+'->'-','/'->'_') 대응
    - 패딩 보정(길이%4==0 되도록 '=' 추가)
    """
    if not b64:
        raise ValueError("Empty base64")

    # 1) data URL 접두사 제거
    b64 = re.sub(r"^data:.*;base64,", "", b64, flags=re.IGNORECASE)

    # 2) 공백/개행 제거
    b64 = re.sub(r"\s+", "", b64)

    # 3) urlsafe 가능성 대응: (우선 그대로 시도, 실패하면 urlsafe로)
    def _pad(s: str) -> str:
        m = len(s) % 4
        return s if m == 0 else s + ("=" * (4 - m))

    try:
        return base64.b64decode(_pad(b64), validate=False)
    except Exception:
        # 그래도 실패하면 urlsafe로 재시도
        return base64.urlsafe_b64decode(_pad(b64))

async def stt_whisper_base64(audio_b64: str, mime: str = "audio/webm") -> str:
    audio_bytes = _normalize_b64(audio_b64)

    # 확장자 추정
    suffix = ".webm" if "webm" in mime else ".wav" if "wav" in mime else ".mp3"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        tmp_path = tmp.name

    # 파일 핸들을 열어서 전달(중요)
    with open(tmp_path, "rb") as fh:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=fh
        )
    return transcript.text
