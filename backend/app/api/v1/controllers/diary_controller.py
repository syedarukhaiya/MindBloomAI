from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.diary import DiaryEntry
from app.models.user import User
from app.schemas.diary import DiaryCreate, DiaryResponse, DiaryUpdate
from app.security.dependencies import get_current_user


router = APIRouter(prefix="/diary", tags=["Diary"])


@router.post("/", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED)
def create_entry(
    data: DiaryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = DiaryEntry(
        user_id=current_user.id,
        title=data.title,
        content=data.content,
        mood=data.mood,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/", response_model=list[DiaryResponse])
def list_entries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.scalars(
        select(DiaryEntry)
        .where(DiaryEntry.user_id == current_user.id)
        .order_by(DiaryEntry.created_at.desc())
    ).all()


@router.get("/{entry_id}", response_model=DiaryResponse)
def get_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = db.get(DiaryEntry, entry_id)

    if entry is None or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Diary entry not found")

    return entry


@router.put("/{entry_id}", response_model=DiaryResponse)
def update_entry(
    entry_id: int,
    data: DiaryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = db.get(DiaryEntry, entry_id)

    if entry is None or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Diary entry not found")

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(entry, field, value)

    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = db.get(DiaryEntry, entry_id)

    if entry is None or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Diary entry not found")

    db.delete(entry)
    db.commit()
