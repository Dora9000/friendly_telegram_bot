from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from bot.utils import commit


class BaseQuery:
    model: DeclarativeMeta

    def __init__(self, session: AsyncSession, model: DeclarativeMeta) -> None:
        self._conn: AsyncSession = session
        self.model = model

    def to_dict(self, entity, exclude_none: bool = False) -> dict:
        return {
            column.name: getattr(entity, column.name)
            for column in entity.__table__.columns
            if not exclude_none or getattr(entity, column.name) is not None
        }

    async def get_entity(self, filters: dict):
        q = select(self.model).where(
            *(getattr(self.model, field) == value for field, value in filters.items())
        )

        res = await self._conn.execute(q)
        return res.scalar_one_or_none()

    @commit
    async def create(self, entity):
        entity = await self._conn.execute(
            insert(self.model)
            .values(self.to_dict(entity, exclude_none=True))
            .returning(self.model)
        )
        return entity.scalar()

    async def get_count(self, filters: dict) -> int:
        q = select(func.count()).select_from(self.model)
        if filters:
            q = q.where(
                *(
                    getattr(self.model, field) == value
                    for field, value in filters.items()
                )
            )
        res = await self._conn.execute(q)
        return res.scalar()

    @commit
    async def update(self, *, values: dict, filters: dict):
        db_entity = await self.get_entity(filters=filters)
        if not db_entity:
            raise Exception(f"Entity with filters: {filters} does not exist")

        try:
            for field, value in values.items():
                setattr(db_entity, field, value)

        except Exception as e:
            raise Exception(f"Entity {db_entity} cant set field for update: {e}")

        return db_entity
