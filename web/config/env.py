# Load database settings from environment variables
from web.utils import load_env_val

POSTGRES_USER = load_env_val('POSTGRES_USER')
POSTGRES_PASSWORD = load_env_val('POSTGRES_PASSWORD')
POSTGRES_HOST = load_env_val('POSTGRES_HOST')
POSTGRES_PORT = load_env_val('POSTGRES_PORT')
POSTGRES_DB = load_env_val('POSTGRES_DB')

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
