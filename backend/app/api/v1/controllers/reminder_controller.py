from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.wellbeing import ReminderCreate, ReminderResponse
from app.security.dependencies import get_current_user
from app.services.reminder_service import (
    create_reminder,
    deactivate_reminder,
    get_user_reminders,
)


router = APIRouter(
    prefix="/reminders",
    tags=["Reminders"],
)


@router.post(
    "/",
    response_model=ReminderResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_reminder(
    data: ReminderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_reminder(db, current_user.id, data)


@router.get(
    "/",
    response_model=list[ReminderResponse],
)
def list_reminders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_user_reminders(db, current_user.id)


@router.delete(
    "/{reminder_id}",
    response_model=ReminderResponse,
)
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    reminder = deactivate_reminder(
        db,
        current_user.id,
        reminder_id,
    )

    if reminder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found",
        )

    return reminder
