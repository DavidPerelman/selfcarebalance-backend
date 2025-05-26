from fastapi import APIRouter, Depends
from app.schemas.mood_entry import MoodEntryCreate
from app.models.user import User
from app.models.mood_entry import MoodEntry
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/mood", tags=["Mood"])


@router.post("/add")
async def add_mood_entry(
    mood: MoodEntryCreate, current_user: User = Depends(get_current_user)
):
    new_mood_entry = MoodEntry(
        client_id=mood.client_id,
        user=current_user,
        mood_score=mood.mood_score,
        emotions=mood.emotions,
        reasons=mood.reasons,
        note=mood.note,
    )

    await new_mood_entry.insert()
    return new_mood_entry
