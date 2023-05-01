import logging
import os

from paramiko import SSHClient
from scp import SCPClient
from sqlalchemy.ext.asyncio import AsyncSession

from bot import settings


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


def upload_to_server(input_filename: str) -> None:
    assert os.path.isfile(f"{settings.LOCAL_INPUTS_DIR}/{input_filename}")

    with SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.connect(
            settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            username=settings.SERVER_USER,
        )

        with SCPClient(ssh.get_transport()) as scp:
            scp.put(
                files=f"{settings.LOCAL_INPUTS_DIR}/{input_filename}",
                remote_path=settings.SERVER_INPUTS_DIR,
            )


def download_from_server(output_filename: str) -> str:
    with SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.connect(
            settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            username=settings.SERVER_USER,
        )

        with SCPClient(ssh.get_transport()) as scp:
            scp.get(
                remote_path=f"{settings.SERVER_OUTPUTS_DIR}/{output_filename}",
                local_path=settings.LOCAL_OUTPUTS_DIR,
            )

            return f"{settings.LOCAL_OUTPUTS_DIR}/{output_filename}"
