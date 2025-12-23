
import asyncio
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import models
from app.core.config import RAG_STORE
from app.rag.store_local import upsert_docs as upsert_local
from app.rag.store_pinecone import upsert_docs as upsert_pinecone

async def run():
    with SessionLocal() as db:
        products = db.query(models.Product).all()
        docs = []
        for p in products:
            text = f"{p.product_name}. {p.description or ''}. Price: {p.price}. CategoryId: {p.category_id}."
            docs.append({
                'id': f'product_{p.product_id}',
                'text': text,
                'metadata': { 'product_id': p.product_id, 'category_id': p.category_id, 'price': float(p.price) }
            })
        if RAG_STORE == 'pinecone':
            await upsert_pinecone(docs)
        else:
            await upsert_local(docs)
        print(f"Ingested {len(docs)} product docs to {RAG_STORE} store")

if __name__ == '__main__':
    asyncio.run(run())
