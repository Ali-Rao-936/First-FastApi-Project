from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import create_access_token, hash_password, verify_password
from app.dependencies import get_db
from app.models.user import User
from app.schemas.user import LoginRequest, LoginResponse, SignupRequest, SignupResponse

router = APIRouter()


@router.post("/signup", response_model=SignupResponse, status_code=201)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    db.add(User(
        email=payload.email,
        name=payload.name,
        username=payload.username,
        hashed_password=hash_password(payload.password),
    ))
    db.commit()
    return SignupResponse(message="Account created successfully")


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"user_id": user.id, "email": user.email})
    return LoginResponse(message="Login successful", token=token)
