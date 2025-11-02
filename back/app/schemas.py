from pydantic import BaseModel
from typing import Optional, List

class ChatIn(BaseModel):
    user_external_id: str
    message: str
    language_hint: Optional[str] = "en"

class ChatOut(BaseModel):
    reply: str
    affinity: int
    energy: int
    relation_level: int
    memory_summary: str = ""

class STTOut(BaseModel):
    text: str

class TTSIn(BaseModel):
    text: str
