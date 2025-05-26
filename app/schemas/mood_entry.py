from typing import List, Optional
from pydantic import BaseModel, Field


class MoodEntryCreate(BaseModel):
    client_id: Optional[str] = None
    mood_score: int = Field(..., ge=1, le=10)
    emotions: List[str]
    reasons: Optional[List[str]] = None
    note: Optional[str] = None
