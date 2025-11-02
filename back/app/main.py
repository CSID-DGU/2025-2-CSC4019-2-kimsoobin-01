from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, chat, audio, ws
from app.db import init_db
from app.utils.logger import setup_logger

setup_logger()
app = FastAPI(title="AI Idol English Teacher API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(chat.router, prefix="/v1/chat", tags=["chat"])
app.include_router(audio.router, prefix="/v1/audio", tags=["audio"])
app.include_router(ws.router, prefix="/ws", tags=["ws"])
