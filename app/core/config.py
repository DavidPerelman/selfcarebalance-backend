from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    mongodb_url: str
    secret_key: str
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    class Config:
        env_file = ".env"


settings = Settings()
