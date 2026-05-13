from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base


class ChatMessage(Base):
    __tablename__ = "n8n_chat_history"

    id         = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, nullable=False, index=True)
    message    = Column(JSONB, nullable=False)
