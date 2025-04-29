from beanie import Document, Link
from pydantic import Field
from datetime import datetime, timezone
from typing import List, Optional
from app.models.user import User


class MoodEntry(Document):
    user: Link[User]
    mood_score: int = Field(..., ge=1, le=10)
    emotions: List[str]  # חובה - חייב להזין רגשות
    reasons: Optional[List[str]] = None
    note: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "mood_entries"
