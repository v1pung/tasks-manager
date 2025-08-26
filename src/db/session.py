from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from src.models import Base
import asyncpg
from fastapi import FastAPI

engine = create_async_engine(settings.DATABASE_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db(app: FastAPI):
    """Инициализация пула соединений и таблиц"""
    app.state.db_pool = await asyncpg.create_pool(settings.DATABASE_URL.replace('postgresql+asyncpg', 'postgresql'))
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
