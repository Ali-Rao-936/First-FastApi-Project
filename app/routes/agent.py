from typing import List

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.config import N8N_WEBHOOK_URL
from app.dependencies import get_db
from app.models.chat_message import ChatMessage
from app.models.user import User
from app.schemas.agent import ChatMessageRead, ChatRequest

router = APIRouter()


@router.get("/chat/messages", response_model=List[ChatMessageRead])
def get_chat_messages(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == str(current_user.id))
        .order_by(ChatMessage.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [
        ChatMessageRead(
            id=r.id,
            role="user" if r.message.get("type") == "human" else "assistant",
            content=r.message.get("data", {}).get("content", ""),
        )
        for r in rows
    ]


@router.delete("/chat/messages")
def clear_chat_messages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == str(current_user.id))
        .delete(synchronize_session=False)
    )
    db.commit()
    return {"deleted": deleted}


@router.delete("/chat/messages/{message_id}")
def delete_chat_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = db.get(ChatMessage, message_id)
    if not row or row.session_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(row)
    db.commit()
    return {"message": "Message deleted"}


@router.post("/chat")
async def chat(
    payload: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                N8N_WEBHOOK_URL,
                json={"message": payload.message, "session_id": str(current_user.id)},
                timeout=30.0,
            )
            response.raise_for_status()
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="n8n webhook timed out")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=f"n8n returned {e.response.status_code}")
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Could not reach n8n webhook")
    return response.json()
