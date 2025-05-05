from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class MoodEntryCreate(BaseModel):
    id: str
    mood_score: int = Field(..., ge=1, le=10)
    emotions: List[str]
    reasons: Optional[List[str]] = None
    note: Optional[str] = None


class MoodEntryResponse(BaseModel):
    id: str
    mood_score: int
    emotions: List[str]
    reasons: Optional[List[str]] = None
    note: Optional[str] = None
    created_at: datetime


class MoodEntryUpdate(BaseModel):
    mood_score: Optional[int] = Field(default=None, ge=1, le=10)
    emotions: Optional[List[str]] = None
    reasons: Optional[List[str]] = None
    note: Optional[str] = None
