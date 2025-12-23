
# app/rag/chat.py

from typing import Any, Dict, List
import asyncio

from app.core.config import OPENAI_API_KEY, RAG_STORE
from app.rag.store_local import retrieve as retrieve_local
from app.rag.store_local import upsert_docs as upsert_local
from app.rag.store_pinecone import retrieve as retrieve_pinecone, upsert_docs as upsert_pinecone


def _build_context(docs: List[Dict[str, Any]] | None) -> str:
    """
    Build a readable context from retrieved docs.
    Each line includes product_id (if available) and a short metadata dump plus text.
    """
    docs = docs or []
    lines: List[str] = []
    for d in docs:
        md = d.get("metadata", {}) or {}
        pid = md.get("product_id", "")
        # try common text fields
        text = (
            d.get("text")
            or d.get("content")
            or d.get("page_content")
            or md.get("description")
            or ""
        )
        lines.append(f"- {pid}: {md} :: {text}")
    return "\n".join(lines)


async def chat_with_rag(query: str, user: Dict[str, Any] | None = None) -> Dict[str, Any]:
    # 1) Retrieve top-k docs from the selected store
    if RAG_STORE == "pinecone":
        docs = await retrieve_pinecone(query, 4)
    else:
        docs = await retrieve_local(query, 4)

    # 2) Build context string (safe quoting / no dangling lines)
    context = _build_context(docs)

    # 3) If no OpenAI key, return a deterministic fallback answer
    if not OPENAI_API_KEY:
        return {
            "contextCount": len(docs),
            "answer": f"""Context (top {len(docs)}):
{context}

Tentative answer: Based on available product info.""",
            "sources": [d.get("metadata", {}) for d in docs],
        }

    # 4) Call OpenAI (non-blocking in async via to_thread)
    try:
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)

        system = "You are a helpful e-commerce assistant. Use provided context."
        prompt = f"""User: {query}

Context:
{context}

Profile: {user or {}}
"""

        # Run the blocking client call in a thread so we don't block the event loop
        resp = await asyncio.to_thread(
            client.chat.completions.create,
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        )

        ans = resp.choices[0].message.content
        return {
            "contextCount": len(docs),
            "answer": ans,
            "sources": [d.get("metadata", {}) for d in docs],
        }

    except Exception as e:
        # Fallback in case OpenAI API fails
        return {
            "contextCount": len(docs),
            "answer": f"""Context (top {len(docs)}):
{context}

Tentative answer: Based on available product info.
(Error: {e})""",
            "sources": [d.get("metadata", {}) for d in docs],
        }
