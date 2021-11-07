from typing import Optional, Callable

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import settings
from models.modelbase import SqlAlchemyBase

ASYNC_SQLALCHEMY_DATABASE_URL = settings.ASYNC_POSTGRES_URL
SQLALCHEMY_DATABASE_URL = settings.POSTGRES_URL

__async_factory: Optional[Callable[[], AsyncSession]] = None


def global_init_db():
    global __async_factory, __factory
    async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)
    __async_factory = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    import models.__all_models
    SqlAlchemyBase.metadata.create_all(bind=engine)


def create_async_session() -> AsyncSession:
    global __async_factory
    if not __async_factory:
        raise Exception("You must call global_init() before using this method.")

    session: AsyncSession = __async_factory()

    return session

