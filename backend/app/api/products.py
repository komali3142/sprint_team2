
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_db
from app.db import models
from app.db.schemas import ProductCreate, ProductOut

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/", response_model=list[ProductOut])
def list_products(category_id: int | None = None, q: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Product)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if q:
        query = query.filter(models.Product.product_name.ilike(f"%{q}%"))
    return query.all()

@router.post("/", response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    p = models.Product(**payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p
