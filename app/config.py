from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


class Settings(BaseSettings):
    jwt_secret_key: str
    access_token_expire_minutes: int
    jwt_encode_algorithm: str
    postgresql_database_password: str
    database_username: str
    database_host: str
    database_port: str
    database_name: str

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")


# creating instance of Settings class, reads in env vars
# each of the key:values is stored as a tuple
settings = Settings()
