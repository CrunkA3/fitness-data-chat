import asyncio
import json
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.llm_service import LLMService

router = APIRouter()


class ChatMessage(BaseModel):
    message: str
    user_id: int = 1  # Default user for demo


class ChatResponse(BaseModel):
    response: str
    chart_data: dict | None = None


@router.post("", response_model=ChatResponse)
async def send_message(
    chat_message: ChatMessage,
    db: Session = Depends(get_db),
) -> ChatResponse:
    """Send a message and get an LLM response."""
    llm_service = LLMService(db=db, user_id=chat_message.user_id)
    try:
        response = await llm_service.process_message(chat_message.message)
        return ChatResponse(
            response=response.get("text", ""),
            chart_data=response.get("chart_data"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/stream")
async def stream_message(
    chat_message: ChatMessage,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    """Stream a chat response using Server-Sent Events."""
    llm_service = LLMService(db=db, user_id=chat_message.user_id)

    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            async for chunk in llm_service.stream_message(chat_message.message):
                data = json.dumps({"chunk": chunk})
                yield f"data: {data}\n\n"
                await asyncio.sleep(0)
        except Exception as e:
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"
        finally:
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/history")
async def get_chat_history(
    user_id: int = 1,
    db: Session = Depends(get_db),
) -> list[dict]:
    """Get chat history for a user."""
    # For a production app, store messages in DB
    # For now, return empty list as a placeholder
    return []
