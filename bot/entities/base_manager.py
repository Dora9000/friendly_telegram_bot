from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from bot.entities.base_query import BaseQuery
from bot.entities.base_validator import BaseValidator


class BaseManager:
    model: DeclarativeMeta
    validator_model: BaseValidator = BaseValidator
    queries: BaseQuery = BaseQuery

    def __init__(self, session: AsyncSession) -> None:
        self._conn: AsyncSession = session
        self.queries = self.queries(session=session, model=self.model)
        self.validator = self.validator_model(session=session, model=self.model)
