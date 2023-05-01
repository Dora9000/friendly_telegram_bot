import os
from pathlib import Path

BOT_TOKEN = os.getenv("BOT_TOKEN", "")


POSTGRES_USER = os.getenv("POSTGRES_USER", "owner")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5433")
POSTGRES_DB = os.getenv("POSTGRES_DB", "core")


SQLALCHEMY_DATABASE_URI = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

MAX_REQUESTS = os.getenv("MAX_REQUESTS", 3)


RABBITMQ_LOGIN = os.getenv("RABBITMQ_LOGIN", "admin")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "87.197.111.68")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 41077)
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "password")


LOCAL_INPUTS_DIR = Path(__file__).parent.parent.resolve() / "inputs"
LOCAL_OUTPUTS_DIR = Path(__file__).parent.parent.resolve() / "outputs"

SERVER_INPUTS_DIR = "/workspace/stable-diffusion/inputs"
SERVER_OUTPUTS_DIR = "/workspace/stable-diffusion/outputs/txt2img-samples/samples"


SERVER_HOST = os.getenv("SERVER_HOST", "78.29.229.186")
SERVER_PORT = os.getenv("SERVER_PORT", 25790)
SERVER_USER = os.getenv("SERVER_USER", "root")
