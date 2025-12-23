
from fastapi import APIRouter
from app.db.schemas import ChatIn, ChatOut
from app.rag.chat import chat_with_rag

router = APIRouter(prefix='/api/chat', tags=['chat'])

@router.post('/', response_model=ChatOut)
async def chat(payload: ChatIn):
    result = await chat_with_rag(payload.query, payload.user or {})
    return result
