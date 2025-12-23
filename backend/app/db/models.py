
from sqlalchemy import Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.db.session import Base

class Category(Base):
    __tablename__ = 'categories'
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    products: Mapped[list['Product']] = relationship('Product', back_populates='category')

class Discount(Base):
    __tablename__ = 'discounts'
    discount_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    discount_type: Mapped[str] = mapped_column(String(10), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    start_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    code: Mapped[str | None] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    products: Mapped[list['Product']] = relationship('Product', back_populates='discount')

class Product(Base):
    __tablename__ = 'products'
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str | None] = mapped_column(String(180), unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.category_id'), nullable=False)
    sku: Mapped[str | None] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(500))
    price: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    discount_id: Mapped[int | None] = mapped_column(ForeignKey('discounts.discount_id'))
    attributes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    category: Mapped['Category'] = relationship('Category', back_populates='products')
    discount: Mapped['Discount'] = relationship('Discount', back_populates='products')
    items: Mapped[list['OrderItem']] = relationship('OrderItem', back_populates='product')

class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(300), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    addresses: Mapped[list['Address']] = relationship('Address', back_populates='user')
    orders: Mapped[list['Order']] = relationship('Order', back_populates='user')

class Address(Base):
    __tablename__ = 'addresses'
    address_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20))
    line1: Mapped[str] = mapped_column(String(200), nullable=False)
    line2: Mapped[str | None] = mapped_column(String(200))
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(60), default='India', nullable=False)
    address_type: Mapped[str] = mapped_column(String(20), nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='addresses')
    ordersShipping: Mapped[list['Order']] = relationship('Order', back_populates='shipping_address', foreign_keys='Order.shipping_address_id')
    ordersBilling: Mapped[list['Order']] = relationship('Order', back_populates='billing_address', foreign_keys='Order.billing_address_id')

class Order(Base):
    __tablename__ = 'orders'
    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), nullable=False)
    order_number: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default='pending', nullable=False)
    subtotal_amount: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    discount_amount: Mapped[float] = mapped_column(Numeric(10,2), default=0, nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(10,2), default=0, nullable=False)
    shipping_amount: Mapped[float] = mapped_column(Numeric(10,2), default=0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default='INR', nullable=False)
    payment_method: Mapped[str | None] = mapped_column(String(50))
    payment_ref: Mapped[str | None] = mapped_column(String(100))
    shipping_address_id: Mapped[int | None] = mapped_column(ForeignKey('addresses.address_id'))
    billing_address_id: Mapped[int | None] = mapped_column(ForeignKey('addresses.address_id'))
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='orders')
    shipping_address: Mapped['Address | None'] = relationship('Address', back_populates='ordersShipping', foreign_keys=[shipping_address_id])
    billing_address: Mapped['Address | None'] = relationship('Address', back_populates='ordersBilling', foreign_keys=[billing_address_id])
    items: Mapped[list['OrderItem']] = relationship('OrderItem', back_populates='order')

class OrderItem(Base):
    __tablename__ = 'order_items'
    order_item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.order_id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.product_id'), nullable=False)
    product_name: Mapped[str] = mapped_column(String(150), nullable=False)
    sku: Mapped[str | None] = mapped_column(String(100))
    unit_price: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    discount_amount: Mapped[float] = mapped_column(Numeric(10,2), default=0, nullable=False)
    total_line_amount: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    order: Mapped['Order'] = relationship('Order', back_populates='items')
    product: Mapped['Product'] = relationship('Product', back_populates='items')

class Admin(Base):
    __tablename__ = 'admins'
    admin_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(300), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    actions: Mapped[list['AdminAction']] = relationship('AdminAction', back_populates='admin')

class AdminAction(Base):
    __tablename__ = 'admin_actions'
    admin_action_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    admin_id: Mapped[int | None] = mapped_column(ForeignKey('admins.admin_id'))
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[int | None] = mapped_column(Integer)
    details: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    admin: Mapped['Admin | None'] = relationship('Admin', back_populates='actions')
