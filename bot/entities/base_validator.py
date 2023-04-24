from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from bot.entities.base_query import BaseQuery


class BaseValidator:
    model: DeclarativeMeta
    queries: BaseQuery = BaseQuery

    def __init__(self, session: AsyncSession, model: DeclarativeMeta) -> None:
        self._conn: AsyncSession = session
        self.model = model
        self.queries = self.queries(session=session, model=self.model)
