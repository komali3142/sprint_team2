
# FastAPI RAG Cart (Auth + React + Pinecone)

Generated: 2025-12-22T09:12:53.387883

This project includes:
- **FastAPI** backend with **JWT auth** (register/login), protected routes, and **RAG chat**.
- **React (Vite)** frontend wired to backend (login, product list, cart, chat).
- **Vector store switch**: local JSON (dev) or **Pinecone** (prod) using Python SDK.

## Quick Start (Windows / PowerShell)

### Backend
```bash
cd backend
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Edit .env: set SECRET_KEY, OPENAI_API_KEY (optional), PINECONE_API_KEY (if using Pinecone)
uvicorn app.main:app --reload
```
Backend: http://localhost:8000
Docs: http://localhost:8000/docs

Seed demo data:
```bash
python app/db/seed.py
```
Ingest products to vector store:
```bash
python app/rag/ingest.py
```

### Frontend
```bash
cd ../frontend
npm install
npm run dev
```
Frontend: http://localhost:5173

## Switch RAG store
- Dev/local JSON: `RAG_STORE=local`
- Pinecone: `RAG_STORE=pinecone` + set `PINECONE_API_KEY`, `PINECONE_INDEX`, `PINECONE_CLOUD` (e.g., aws), `PINECONE_REGION` (e.g., us-east-1).
