import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "")


POSTGRES_USER = os.getenv("POSTGRES_USER", "owner")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5433")
POSTGRES_DB = os.getenv("POSTGRES_DB", "core")


SQLALCHEMY_DATABASE_URI = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

MAX_REQUESTS = os.getenv("MAX_REQUESTS", 3)
