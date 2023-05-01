from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String

from ..constants import StatusEnum
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    first_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    init_k = Column(Numeric(precision=5, scale=2), nullable=True)
    grad_k = Column(Numeric(precision=5, scale=2), nullable=True)
    created = Column(DateTime(timezone=False), server_default=func.now())


class Photo(Base):
    __tablename__ = "photos"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    file_id = Column(String, nullable=False)
    file_unique_id = Column(String, nullable=False)
    height = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    file_size = Column(Integer, nullable=False)
    prompt = Column(String, nullable=False)
    created = Column(DateTime(timezone=False), server_default=func.now())


class PhotoToUser(Base):
    __tablename__ = "photo_to_user"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    photo_id = Column(
        BigInteger, ForeignKey("photos.id", ondelete="CASCADE"), nullable=False
    )
    result_photo_name = Column(String, nullable=True)
    status = Column(String, nullable=False, default=StatusEnum.PENDING.value)
    chat_id = Column(BigInteger, nullable=False)
    message_id = Column(BigInteger, nullable=False)
    created = Column(DateTime(timezone=False), server_default=func.now())
