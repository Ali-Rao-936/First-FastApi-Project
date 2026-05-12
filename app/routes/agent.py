import httpx
from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user
from app.core.config import N8N_WEBHOOK_URL
from app.models.user import User
from app.schemas.agent import ChatRequest

router = APIRouter()


@router.post("/chat")
async def chat(
    payload: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                N8N_WEBHOOK_URL,
                json={"message": payload.message},
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
