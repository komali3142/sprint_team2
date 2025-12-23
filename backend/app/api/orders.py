
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_db, get_current_user
from app.db import models
from app.db.schemas import CheckoutIn, OrderOut

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/checkout", response_model=OrderOut)
def checkout(payload: CheckoutIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    subtotal = sum(float(i.unit_price) * i.quantity for i in payload.items)
    discount = 0.0
    tax = 0.0
    shipping = 0.0
    total = subtotal - discount + tax + shipping
    order_number = f"ORD-{int(__import__('time').time()*1000)}"

    order = models.Order(
        user_id=user.user_id,
        order_number=order_number,
        status='pending',
        subtotal_amount=subtotal,
        discount_amount=discount,
        tax_amount=tax,
        shipping_amount=shipping,
        total_amount=total,
        shipping_address_id=payload.shipping_address_id,
        billing_address_id=payload.billing_address_id,
    )
    db.add(order)
    db.flush()

    for it in payload.items:
        db.add(models.OrderItem(
            order_id=order.order_id,
            product_id=it.product_id,
            product_name=it.product_name,
            sku=it.sku,
            unit_price=it.unit_price,
            quantity=it.quantity,
            discount_amount=0,
            total_line_amount=float(it.unit_price) * it.quantity
        ))
        prod = db.query(models.Product).filter_by(product_id=it.product_id).first()
        if prod:
            prod.stock = max(0, prod.stock - it.quantity)

    db.commit()
    db.refresh(order)
    return order
