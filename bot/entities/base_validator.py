from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta


class BaseValidator:
    model: DeclarativeMeta

    def __init__(self, session: AsyncSession, model: DeclarativeMeta) -> None:
        self._conn: AsyncSession = session
        self.model = model
