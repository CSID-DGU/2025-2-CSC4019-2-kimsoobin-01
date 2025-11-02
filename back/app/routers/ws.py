from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.sentiment import sentiment_score
from app.utils.emotion import EmotionState
from app.services.persona import build_persona_block, inject_dynamic_state
from app.services.llm_gemini import gemini_complete

router = APIRouter()

@router.websocket("/dialogue")
async def dialogue_socket(ws: WebSocket):
    await ws.accept()
    state = EmotionState()
    try:
        await ws.send_text("CONNECTED: Send text messages; I reply token-wise.")
        while True:
            text = await ws.receive_text()
            s = sentiment_score(text)
            state.update_with(text, s)
            level = state.to_level()

            system = build_persona_block()
            dynamic = inject_dynamic_state(state.affinity, state.energy, level, "")
            prompt = f"{system}\n{dynamic}\nUser: {text}\nAssistant:"

            # 간단 스트리밍 흉내: 문장을 절단해서 전송
            reply = await gemini_complete(prompt)
            for chunk in reply.split(" "):
                await ws.send_text(chunk)
        # (실서비스에선 LLM 스트리밍 API 사용 권장)
    except WebSocketDisconnect:
        return
