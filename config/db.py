import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL_ALEMBIC = os.getenv("DATABASE_URL_ALEMBIC")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(
    autoflush=False, autocommit=False, bind=engine
)


class Base(DeclarativeBase):
    pass


class DatabaseSessionManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        return self.session

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()


async def get_db():
    async with DatabaseSessionManager(SessionLocal) as session:
        yield session
