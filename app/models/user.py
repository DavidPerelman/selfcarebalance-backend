from datetime import datetime, timezone
from typing import Optional
from beanie import Document
from pydantic import EmailStr, Field


class User(Document):
    email: EmailStr
    username: str
    profile_picture: Optional[str] = None
    is_oauth_user: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
