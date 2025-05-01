from typing import Optional
from beanie import Document
from pydantic import EmailStr


class User(Document):
    email: EmailStr
    username: str
    hashed_password: Optional[str] = None  # מאפשר חיבור מגוגל בלי סיסמה
    full_name: Optional[str] = None
    profile_picture: Optional[str] = None
    is_oauth_user: bool = False

    class Settings:
        name = "users"
