"""FastAPI application entry point for LexSpend."""

from __future__ import annotations

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.database import create_db_and_tables, AsyncSession, get_session, asynccontextmanager

app = FastAPI(
    title="LexSpend API",
    description="AI-powered legal invoice tracking and spend management",
    version="0.1.0",
    redirect_slashes=False
)

# ---------------------------------------------------------------------------
# CORS – allow the Next.js dev server and any additional configured origins
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. FastAPI Lifespan to initialize tables asynchronously on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
  await create_db_and_tables()
  yield


app = FastAPI(lifespan=lifespan)

# 7. Example asynchronous endpoint using the async session
@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)):
  # You would use `await session.exec(...)` for database queries
  return {"status": "healthy", "database": "async-connected"}

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(api_router, prefix="/api/v1")
