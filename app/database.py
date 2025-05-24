from datetime import datetime

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy import func, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, class_mapper

from .config import PG_URL



class Base(AsyncAttrs, DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.

    """

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )

    def to_dict(self) -> dict:
        columns = class_mapper(self.__class__).columns
        return {column.key: getattr(self, column.key) for column in columns}


engine = create_async_engine(url=PG_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
