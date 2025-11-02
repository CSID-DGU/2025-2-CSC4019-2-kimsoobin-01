from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Memory, Turn, User
from typing import Optional
from app.services.persona import build_persona_block
from app.services.llm_gemini import gemini_complete

async def get_or_create_user(session:AsyncSession, external_user_id:str) -> User:
    q = await session.execute(select(User).where(User.external_user_id==external_user_id))
    user = q.scalar_one_or_none()
    if not user:
        user = User(external_user_id=external_user_id)
        session.add(user)
        await session.flush()
    return user

async def recent_memory(session:AsyncSession, user_id:int) -> Optional[Memory]:
    q = await session.execute(select(Memory).where(Memory.user_id==user_id).order_by(Memory.id.desc()).limit(1))
    return q.scalar_one_or_none()

async def save_turn(session:AsyncSession, user_id:int, role:str, content:str):
    session.add(Turn(user_id=user_id, role=role, content=content))
    await session.flush()

async def summarize_and_save(session:AsyncSession, user_id:int) -> Memory:
    # 최근 20턴 요약
    q = await session.execute(select(Turn).where(Turn.user_id==user_id).order_by(Turn.id.desc()).limit(20))
    turns = list(reversed(q.scalars().all()))
    transcript = "\n".join([f"{t.role.upper()}: {t.content}" for t in turns])

    system = build_persona_block() + "\nSummarize the key facts about the user in <=60 Korean characters each, 3~5 bullets."
    prompt = f"{system}\n\n=== Conversation Excerpt ===\n{transcript}\n\n=== Task ===\nMake a compact memory list."
    summary = await gemini_complete(prompt)

    mem = Memory(user_id=user_id, summary=summary, level=1)
    session.add(mem)
    await session.flush()
    return mem
