from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from bot.settings import SQLALCHEMY_DATABASE_URI

Base = declarative_base()


async def create_async_database():
    engine = create_async_engine(url=SQLALCHEMY_DATABASE_URI, echo=True)

    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)
    return async_session
