
import json, os
from app.core.config import RAG_STORE_PATH
from app.rag.embedding import embed_texts

async def upsert_docs(docs: list[dict]):
    embeddings = await embed_texts([d['text'] for d in docs])
    items = [dict(d, embedding=e) for d,e in zip(docs, embeddings)]
    cur = []
    if os.path.exists(RAG_STORE_PATH):
        cur = json.loads(open(RAG_STORE_PATH,'r',encoding='utf-8').read())
    cur.extend(items)
    open(RAG_STORE_PATH,'w',encoding='utf-8').write(json.dumps(cur, ensure_ascii=False))

async def retrieve(query: str, top_k: int = 4) -> list[dict]:
    if not os.path.exists(RAG_STORE_PATH):
        return []
    store = json.loads(open(RAG_STORE_PATH,'r',encoding='utf-8').read())
    qemb = (await embed_texts([query]))[0]
    def cosine(a,b):
        import math
        dot = sum(x*y for x,y in zip(a,b))
        na = math.sqrt(sum(x*x for x in a))
        nb = math.sqrt(sum(y*y for y in b))
        return dot / (na*nb + 1e-9)
    for it in store:
        it['score'] = cosine(qemb, it.get('embedding', [0]*256))
    store.sort(key=lambda x: x.get('score',0), reverse=True)
    return store[:top_k]
