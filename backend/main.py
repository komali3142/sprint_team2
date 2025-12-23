
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.db.session import engine
from app.db import models

from app.api.products import router as products_router
from app.api.categories import router as categories_router
from app.api.orders import router as orders_router
from app.api.chat import router as chat_router
from app.api.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="FastAPI RAG Cart (Auth)", lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <head><title>RAG Cart API</title></head>
      <body style="font-family: system-ui, -apple-system, Segoe UI, Arial; line-height:1.6; max-width: 760px; margin: 2rem auto;">
        <h1>🛍️ E-Commerce API is Running</h1>
        <p>Explore the interactive API docs at /docs/docs</a>.</p>
        <ul>
          <li><code>/auth</code> — register &amp; login</li>
          <li><code>/products</code> — manage products</li>
          <li><code>/categories</code> — product categories</li>
          <li><code>/orders</code> — create &amp; fetch orders</li>
          <li><code>/chat</code> — RAG chat endpoint</li>
        </ul>
      </body>
    </html>
    """


app.include_router(auth_router)
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(orders_router)
app.include_router(chat_router)
