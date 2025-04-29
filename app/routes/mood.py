from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.mood_entry import MoodEntryCreate, MoodEntryResponse, MoodEntryUpdate
from app.models.user import User
from app.models.mood_entry import MoodEntry
from app.services.auth import get_current_user

router = APIRouter(prefix="/mood", tags=["Mood"])

POSITIVE_EMOTIONS = [
    "אמון",
    "אמפתיה",
    "אומץ",
    "אדיבות",
    "חשיבות עצמית",
    "שמחה",
    "שלווה",
    "אהבה",
    "התרגשות",
    "סקרנות",
    "תקווה",
    "הכרת תודה",
    "גאווה",
    "רוגע",
    "סיפוק",
    "אופטימיות",
    "השראה",
    "הנאה",
    "חמלה",
    "ביטחון",
]

NEGATIVE_EMOTIONS = [
    "עצב",
    "כעס",
    "פחד",
    "בדידות",
    "לחץ",
    "חרדה",
    "אכזבה",
    "קנאה",
    "בושה",
    "ייאוש",
    "עייפות",
    "בלבול",
    "חוסר ערך",
    "גועל",
    "אשמה",
    "מבוכה",
    "החמצה",
    "דאגה",
    "שנאה",
    "תסכול",
    "חוסר אונים",
]


@router.get("/emotions")
async def get_emotions():
    return {
        "positive_emotions": POSITIVE_EMOTIONS,
        "negative_emotions": NEGATIVE_EMOTIONS,
    }


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


@router.put("/{id}", response_model=MoodEntryResponse)
async def update_mood_entry(
    id: str, mood: MoodEntryUpdate, current_user: User = Depends(get_current_user)
):
    mood_entry = await MoodEntry.get(id)

    if not mood_entry:
        raise HTTPException(status_code=404, detail="Mood entry not found")

    await mood_entry.fetch_link(MoodEntry.user)

    if mood_entry.user.id != current_user.id:
        raise HTTPException(status_code=403, detail="You cannot edit this mood entry")

    if mood.mood_score is not None:
        mood_entry.mood_score = mood.mood_score
    if mood.emotions is not None:
        mood_entry.emotions = mood.emotions
    if mood.reasons is not None:
        mood_entry.reasons = mood.reasons
    if mood.note is not None:
        mood_entry.note = mood.note

    await mood_entry.save()

    return MoodEntryResponse(
        id=str(mood_entry.id),
        mood_score=mood_entry.mood_score,
        emotions=mood_entry.emotions,
        reasons=mood_entry.reasons,
        note=mood_entry.note,
        created_at=mood_entry.created_at,
    )
