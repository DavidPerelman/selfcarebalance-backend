from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    environment: str = Field(..., alias="ENVIRONMENT")
    secret_key: str
    mongodb_url: str
    google_client_id: str
    google_client_secret: str
    google_redirect_uri_local: str
    google_redirect_uri_prod: str

    @property
    def google_redirect_uri(self) -> str:
        return (
            self.google_redirect_uri_prod
            if self.environment == "production"
            else self.google_redirect_uri_local
        )
    
    @property
    def frontend_url(self) -> str:
        return (
        'http://localhost:3000'
        if self.environment == "development"
        else "https://selfcarebalance.vercel.app"
        )

    class Config:
        env_file = ".env"


settings = Settings()
