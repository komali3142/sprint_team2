
from app.core.config import PINECONE_API_KEY, PINECONE_INDEX, PINECONE_CLOUD, PINECONE_REGION
from app.rag.embedding import embed_texts

# Pinecone SDK
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key=PINECONE_API_KEY) if PINECONE_API_KEY else None

def ensure_index(dimension: int):
    if not pc:
        raise RuntimeError('PINECONE_API_KEY not set')
    names = [idx.name for idx in pc.list_indexes()]
    if PINECONE_INDEX not in names:
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=dimension,
            metric='cosine',
            spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION)
        )

async def upsert_docs(docs: list[dict]):
    if not pc:
        raise RuntimeError('Pinecone client not initialized')
    # compute embeddings
    embeddings = await embed_texts([d['text'] for d in docs])
    dim = len(embeddings[0]) if embeddings else 256
    ensure_index(dim)
    index = pc.Index(PINECONE_INDEX)
    vectors = []
    for d,e in zip(docs, embeddings):
        vectors.append((d['id'], e, d.get('metadata', {})))
    index.upsert(vectors=vectors)

async def retrieve(query: str, top_k: int = 4) -> list[dict]:
    if not pc:
        return []
    index = pc.Index(PINECONE_INDEX)
    qemb = (await embed_texts([query]))[0]
    res = index.query(vector=qemb, top_k=top_k, include_metadata=True)
    out = []
    for m in res.matches:
        out.append({ 'id': m.id, 'text': '', 'metadata': m.metadata, 'score': m.score })
    return out
