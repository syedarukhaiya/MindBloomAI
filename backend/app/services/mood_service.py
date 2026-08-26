from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.mood import MoodEntry
from app.schemas.mood import MoodCreate


def create_mood(db: Session, user_id: int, data: MoodCreate) -> MoodEntry:
    entry = MoodEntry(
        user_id=user_id,
        mood=data.mood,
        note=data.note,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_user_moods(db: Session, user_id: int) -> list[MoodEntry]:
    result = db.execute(
        select(MoodEntry)
        .where(MoodEntry.user_id == user_id)
        .order_by(MoodEntry.created_at.desc())
    )
    return list(result.scalars().all())
