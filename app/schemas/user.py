from datetime import datetime

from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    email: EmailStr
    name: str
    username: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class SignupResponse(BaseModel):
    message: str


class LoginResponse(BaseModel):
    message: str
    token: str


class UserOut(BaseModel):
    id: int
    email: str
    name: str
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}
