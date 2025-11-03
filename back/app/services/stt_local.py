# app/services/stt_local.py
import base64, re, tempfile, os
from faster_whisper import WhisperModel

_model = None

def _normalize_b64(b64: str) -> bytes:
    b64 = re.sub(r"^data:.*;base64,", "", b64, flags=re.IGNORECASE)
    b64 = re.sub(r"\s+", "", b64)
    pad = (-len(b64)) % 4
    if pad: b64 += "=" * pad
    return base64.b64decode(b64)

def _get_model():
    global _model
    if _model is None:
        # 모델 크기: tiny/base/small/medium/large-v3 (크기↑=정확도↑=속도↓)
        _model = WhisperModel("small", device="cpu", compute_type="int8")
    return _model

async def stt_local_base64(audio_b64: str, mime: str = "audio/webm") -> str:
    audio_bytes = _normalize_b64(audio_b64)
    suffix = ".webm" if "webm" in mime else ".wav" if "wav" in mime else ".mp3"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        path = tmp.name

    try:
        model = _get_model()
        segments, _ = model.transcribe(path, vad_filter=True, language=None)  # 자동 언어 감지
        text = "".join([seg.text for seg in segments]).strip()
        return text
    finally:
        try: os.remove(path)
        except: pass
