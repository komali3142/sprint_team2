
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import models
from app.db.schemas import RegisterIn, TokenOut
from app.core.security import get_db, get_password_hash, verify_password, create_access_token

router = APIRouter(prefix='/api/auth', tags=['auth'])

@router.post('/register', response_model=TokenOut)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(email=payload.email).first():
        raise HTTPException(status_code=400, detail='Email already registered')
    user = models.User(
        name=payload.name,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        phone=payload.phone
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": user.user_id})
    return TokenOut(access_token=token)

@router.post('/login', response_model=TokenOut)
def login(payload: RegisterIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token({"sub": user.user_id})
    return TokenOut(access_token=token)
