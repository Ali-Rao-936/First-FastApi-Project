from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatMessageRead(BaseModel):
    id:      int
    role:    str
    content: str

    model_config = {"from_attributes": True}
