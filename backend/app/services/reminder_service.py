from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.reminder import Reminder
from app.schemas.wellbeing import ReminderCreate


def create_reminder(
    db: Session,
    user_id: int,
    data: ReminderCreate,
) -> Reminder:
    reminder = Reminder(
        user_id=user_id,
        title=data.title,
        message=data.message,
        reminder_time=data.reminder_time,
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    return reminder


def get_user_reminders(
    db: Session,
    user_id: int,
) -> list[Reminder]:
    result = db.execute(
        select(Reminder)
        .where(
            Reminder.user_id == user_id,
            Reminder.is_active.is_(True),
        )
        .order_by(Reminder.reminder_time.asc())
    )

    return list(result.scalars().all())


def deactivate_reminder(
    db: Session,
    user_id: int,
    reminder_id: int,
) -> Reminder | None:
    reminder = db.get(Reminder, reminder_id)

    if reminder is None or reminder.user_id != user_id:
        return None

    reminder.is_active = False
    db.commit()
    db.refresh(reminder)

    return reminder
