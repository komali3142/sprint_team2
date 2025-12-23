
from pydantic import BaseModel
from typing import Optional, List

class CategoryCreate(BaseModel):
    category_name: str
    description: Optional[str] = None

class CategoryOut(BaseModel):
    category_id: int
    category_name: str
    description: Optional[str]
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    product_name: str
    slug: Optional[str] = None
    category_id: int
    sku: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: float
    stock: int = 0
    discount_id: Optional[int] = None
    attributes: Optional[str] = None

class ProductOut(BaseModel):
    product_id: int
    product_name: str
    price: float
    stock: int
    category_id: int
    discount_id: Optional[int]
    description: Optional[str]
    class Config:
        from_attributes = True

class OrderItemIn(BaseModel):
    product_id: int
    product_name: str
    sku: Optional[str] = None
    unit_price: float
    quantity: int

class CheckoutIn(BaseModel):
    user_id: int
    items: List[OrderItemIn]
    shipping_address_id: Optional[int] = None
    billing_address_id: Optional[int] = None

class OrderOut(BaseModel):
    order_id: int
    order_number: str
    status: str
    total_amount: float
    class Config:
        from_attributes = True

# Auth
class RegisterIn(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[str] = None

class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class ChatIn(BaseModel):
    query: str
    user: Optional[dict] = None

class ChatOut(BaseModel):
    contextCount: int
    answer: str
    sources: list
