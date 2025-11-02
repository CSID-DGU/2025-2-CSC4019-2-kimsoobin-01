import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", "8000"))
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")
    # Persona
    PERSONA_NAME = os.getenv("PERSONA_NAME", "Luca")
    PERSONA_AGE = os.getenv("PERSONA_AGE", "19")
    PERSONA_ROLE = os.getenv("PERSONA_ROLE", "K-POP idol and study partner")
    PERSONA_STYLE = os.getenv("PERSONA_STYLE", "Bright, positive, encouraging")
    PERSONA_VALUES = os.getenv("PERSONA_VALUES", "Effort & teamwork")
    PERSONA_GOAL = os.getenv("PERSONA_GOAL", "Grow together while studying English")

settings = Settings()
