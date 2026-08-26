from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.diary import DiaryEntry
from app.models.user import User
from app.schemas.diary import (
    DiaryCreate,
    DiaryResponse,
    DiaryUpdate,
)
from app.security.dependencies import get_current_user


router = APIRouter(
    prefix="/diary",
    tags=["Diary"],
)


# ============================================================
# CREATE DIARY ENTRY
# ============================================================


@router.post(
    "/",
    response_model=DiaryResponse,
    status_code=status.HTTP_201_CREATED,
)
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

    try:
        db.commit()
        db.refresh(entry)
    except Exception:
        db.rollback()
        raise

    return entry


# ============================================================
# LIST USER DIARY ENTRIES
# ============================================================


@router.get(
    "/",
    response_model=list[DiaryResponse],
)
def list_entries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entries = db.scalars(
        select(DiaryEntry)
        .where(
            DiaryEntry.user_id == current_user.id
        )
        .order_by(
            DiaryEntry.created_at.desc()
        )
    ).all()

    return entries


# ============================================================
# GET SINGLE DIARY ENTRY
# ============================================================


@router.get(
    "/{entry_id}",
    response_model=DiaryResponse,
)
def get_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = db.scalar(
        select(DiaryEntry).where(
            DiaryEntry.id == entry_id,
            DiaryEntry.user_id == current_user.id,
        )
    )

    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary entry not found",
        )

    return entry


# ============================================================
# UPDATE DIARY ENTRY
# ============================================================


@router.put(
    "/{entry_id}",
    response_model=DiaryResponse,
)
def update_entry(
    entry_id: int,
    data: DiaryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = db.scalar(
        select(DiaryEntry).where(
            DiaryEntry.id == entry_id,
            DiaryEntry.user_id == current_user.id,
        )
    )

    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary entry not found",
        )

    updates = data.model_dump(
        exclude_unset=True
    )

    for field, value in updates.items():
        setattr(entry, field, value)

    try:
        db.commit()
        db.refresh(entry)
    except Exception:
        db.rollback()
        raise

    return entry


# ============================================================
# DELETE DIARY ENTRY
# ============================================================


@router.delete(
    "/{entry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = db.scalar(
        select(DiaryEntry).where(
            DiaryEntry.id == entry_id,
            DiaryEntry.user_id == current_user.id,
        )
    )

    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary entry not found",
        )

    try:
        db.delete(entry)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return None