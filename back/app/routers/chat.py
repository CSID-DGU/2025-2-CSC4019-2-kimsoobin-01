from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import AsyncSessionLocal
from app.schemas import ChatIn, ChatOut
from app.services.persona import build_persona_block, inject_dynamic_state
from app.services.sentiment import sentiment_score
from app.utils.emotion import EmotionState
from app.services.memory import get_or_create_user, recent_memory, save_turn, summarize_and_save
from app.services.llm_gemini import gemini_complete

router = APIRouter()

async def get_session():
    async with AsyncSessionLocal() as s:
        yield s

@router.post("/", response_model=ChatOut)
async def chat(payload: ChatIn, session: AsyncSession = Depends(get_session)):
    try:
        user = await get_or_create_user(session, payload.user_external_id)

        # 1) 감정/상태 조회(간단히 새로 생성; 필요시 Redis로 세션 관리 가능)
        state = EmotionState()

        # 2) 메모리 불러오기
        mem = await recent_memory(session, user.id)
        mem_summary = mem.summary if mem else ""

        # 3) 감성 분석 -> 상태 업데이트
        s = sentiment_score(payload.message)
        state.update_with(payload.message, s)
        level = state.to_level()

        # 4) 시스템 프롬프트 구성
        system = build_persona_block()
        dynamic = inject_dynamic_state(state.affinity, state.energy, level, mem_summary)

        # 5) 유저 입력 + 역할에 맞는 프롬프트
        prompt = (
            f"{system}\n{dynamic}\n"
            "Instruction: Respond in a friendly, scaffolded way. If user makes mistakes, give 1 tiny hint first, then an example. "
            "Keep sentences short. Mix simple English with a tiny bit of Korean if needed for clarity.\n\n"
            f"User says: {payload.message}\n"
            "Now reply as the persona."
        )
        reply = await gemini_complete(prompt)

        # 6) 저장
        await save_turn(session, user.id, "user", payload.message)
        await save_turn(session, user.id, "assistant", reply)

        # 7) 세션 종료/주기적으로 요약
        # 간단히: 매 10턴마다 요약 저장
        # (프로덕션에서는 실제 턴 카운트 체크/세션 종료 시점에 호출)
        # 여기선 무조건 최신 요약 갱신하도록 구현(데모 목적)
        mem = await summarize_and_save(session, user.id)

        await session.commit()
        return ChatOut(
            reply=reply,
            affinity=state.affinity, energy=state.energy,
            relation_level=level, memory_summary=mem.summary
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(500, f"Chat failed: {e}")
