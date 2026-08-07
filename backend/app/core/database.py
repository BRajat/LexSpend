from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_db_url


# 1. Load database URL from settings and fall back to a local SQLite file.
DATABASE_URL = get_db_url()


# 2. Create the asynchronous engine
# set echo=True, only when debugging SQL queries
# connect args should be db specific.
# no need to pass check_same_thread when db = sqlite
async_engine = create_async_engine(
    DATABASE_URL, 
    echo=False, 
    # connect_args={"check_same_thread": False}
)


# 3. Define the asynchronous DDL creation function
async def create_db_and_tables():
    pass
    print("DATABASE URL ===========>", DATABASE_URL)
    async with async_engine.begin() as conn:
      # run_sync executes the synchronous metadata create_all inside the async connection context
      await conn.run_sync(SQLModel.metadata.create_all)


# 5. Configure the asynchronous session maker
async_session_maker = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# 6. True async dependency injection generator
async def get_session() -> AsyncGenerator[AsyncSession, None]:
  async with async_session_maker() as session:
    yield session
