from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    mongodb_url: str = Field(alias="MONGODB_URL")

    class Config:
        env_file = ".env"


settings = Settings()
