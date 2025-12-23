
from app.db.session import engine, SessionLocal
from app.db import models
from datetime import datetime, timedelta

models.Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    electronics = db.query(models.Category).filter_by(category_name='Electronics').first()
    if not electronics:
        electronics = models.Category(category_name='Electronics', description='Mobiles, laptops, accessories')
        db.add(electronics)
    apparel = db.query(models.Category).filter_by(category_name='Apparel').first()
    if not apparel:
        apparel = models.Category(category_name='Apparel', description='Clothing and fashion')
        db.add(apparel)

    disc = models.Discount(
        discount_type='percent', value=10,
        start_at=datetime.utcnow(), end_at=datetime.utcnow() + timedelta(days=30),
        code='WELCOME10', is_active=True
    )
    db.add(disc)
    db.flush()

    p1 = models.Product(
        product_name='Smartphone X', slug='smartphone-x', category_id=electronics.category_id,
        sku='SMX-64-BLK', description='64GB, Black', price=29999, stock=50,
        discount_id=disc.discount_id, attributes='{"ram":"6GB","storage":"64GB"}'
    )
    db.add(p1)
    p2 = models.Product(
        product_name='Denim Jacket', slug='denim-jacket', category_id=apparel.category_id,
        sku='DJ-IND-M', description='Indigo, Medium', price=2499, stock=100,
        attributes='{"size":"M"}'
    )
    db.add(p2)

    # demo user
    from app.core.security import get_password_hash
    u = models.User(name='Komali', email='komali@example.com', password_hash=get_password_hash('Password@123'))
    db.add(u)

    db.commit()
    print('Seeded categories, discount, products, and demo user')
