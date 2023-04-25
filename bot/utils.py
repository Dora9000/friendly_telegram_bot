import logging

from sqlalchemy.ext.asyncio import AsyncSession


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def save_execute(f):
    async def wrapper(session: AsyncSession, *args, **kwargs):
        try:
            return await f(session, *args, **kwargs)
        except Exception as e:
            await session.rollback()
            logging.error(e)

    return wrapper


def commit(f):
    async def wrapper(self, **kwargs):
        session = self._conn

        try:
            res = await f(self, **kwargs)
            await session.commit()
            return res

        except Exception as e:
            await session.rollback()
            # logging.error(e)
            raise

    return wrapper


async def save_commit(session: AsyncSession):
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        logging.error(e)


import contextlib


@contextlib.contextmanager
def transaction(session):
    if not session.in_transaction():
        with session.begin():
            yield
    else:
        yield
