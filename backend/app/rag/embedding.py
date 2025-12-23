
from app.core.config import OPENAI_API_KEY

async def embed_texts(texts: list[str]) -> list[list[float]]:
    if not OPENAI_API_KEY:
        emb = []
        for t in texts:
            v = [(ord(t[i % len(t)]) if len(t)>0 else 0)/255.0 for i in range(256)]
            emb.append(v)
        return emb
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        resp = client.embeddings.create(model='text-embedding-3-small', input=texts)
        return [d.embedding for d in resp.data]
    except Exception:
        return await embed_texts(texts[:])
