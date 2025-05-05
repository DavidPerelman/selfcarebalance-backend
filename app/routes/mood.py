from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date, datetime

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
        client_id=mood.id,
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
async def get_my_moods(
    from_date: Optional[date] = Query(None, alias="from"),
    to_date: Optional[date] = Query(None, alias="to"),
    current_user: User = Depends(get_current_user),
):
    query = MoodEntry.find(MoodEntry.user.id == current_user.id)

    if from_date:
        query = query.find(
            MoodEntry.created_at >= datetime.combine(from_date, datetime.min.time())
        )
    if to_date:
        query = query.find(
            MoodEntry.created_at <= datetime.combine(to_date, datetime.max.time())
        )

    moods = await query.to_list()

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


@router.delete("/{id}")
async def delete_mood_entry(id: str, current_user: User = Depends(get_current_user)):
    mood_entry = await MoodEntry.get(id)

    if not mood_entry:
        raise HTTPException(status_code=404, detail="Mood entry not found")

    await mood_entry.fetch_link(MoodEntry.user)

    if mood_entry.user.id != current_user.id:
        raise HTTPException(status_code=403, detail="You cannot delete this mood entry")

    await mood_entry.delete()
    return {"detail": "Mood entry deleted successfully"}

@router.delete("/all")
async def delete_all_moods(current_user: User = Depends(get_current_user)):
    query = MoodEntry.find(MoodEntry.user.id == current_user.id)

    await query.delete()

    return {"detail": "Moods deleted successfully"}

@router.post("/import", response_model=List[MoodEntryResponse])
async def import_moods(moods: List[MoodEntryCreate], 
                       current_user: User = Depends(get_current_user)):
    existing = await MoodEntry.find(MoodEntry.user.id == current_user.id).to_list()

    existing_ids = {entry.client_id for entry in existing}
    new_moods = [m for m in moods if m.id not in existing_ids]
    
    results = []

    for mood in new_moods:
        new_entry = MoodEntry(
            client_id=mood.id,
            user=current_user,
            mood_score=mood.mood_score,
            emotions=mood.emotions,
            reasons=mood.reasons,
            note=mood.note,
        )
        await new_entry.insert()

        results.append(
            MoodEntryResponse(
                id=str(new_entry.id),
                mood_score=new_entry.mood_score,
                emotions=new_entry.emotions,
                reasons=new_entry.reasons,
                note=new_entry.note,
                created_at=new_entry.created_at,
            )
        )

    return results





