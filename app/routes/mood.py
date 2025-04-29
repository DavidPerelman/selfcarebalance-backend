from typing import List
from fastapi import APIRouter, Depends

from app.schemas.mood_entry import MoodEntryCreate, MoodEntryResponse
from app.models.user import User
from app.models.mood_entry import MoodEntry
from app.services.auth import get_current_user

router = APIRouter(prefix="/mood", tags=["Mood"])


@router.post("/add", response_model=MoodEntryResponse)
async def add_mood_entry(
    mood: MoodEntryCreate, current_user: User = Depends(get_current_user)
):
    new_mood_entry = MoodEntry(
        user=current_user,
        mood_score=mood.mood_score,
        emotions=mood.emotions,
        reasons=mood.reasons,
        note=mood.note,
    )

    await new_mood_entry.insert()

    return MoodEntryResponse(
        id=str(new_mood_entry.id),
        mood_score=new_mood_entry.mood_score,
        emotions=new_mood_entry.emotions,
        reasons=new_mood_entry.reasons,
        note=new_mood_entry.note,
        created_at=new_mood_entry.created_at,
    )


@router.get("/my", response_model=List[MoodEntryResponse])
async def get_my_moods(current_user: User = Depends(get_current_user)):
    moods = await MoodEntry.find(MoodEntry.user.id == current_user.id).to_list()

    return [
        MoodEntryResponse(
            id=str(mood.id),
            mood_score=mood.mood_score,
            emotions=mood.emotions,
            reasons=mood.reasons,
            note=mood.note,
            created_at=mood.created_at,
        )
        for mood in moods
    ]
