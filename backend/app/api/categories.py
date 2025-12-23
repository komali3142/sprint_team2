
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_db
from app.db import models
from app.db.schemas import CategoryCreate, CategoryOut

router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

@router.post("/", response_model=CategoryOut)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    c = models.Category(**payload.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c
