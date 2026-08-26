from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.mood import MoodCreate, MoodResponse
from app.services.mood_service import create_mood, get_user_moods
from app.security.dependencies import get_current_user

router = APIRouter(prefix="/moods", tags=["Mood"])


@router.post(
    "/",
    response_model=MoodResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_mood(
    data: MoodCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_mood(db, current_user.id, data)


@router.get("/", response_model=list[MoodResponse])
def list_moods(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_user_moods(db, current_user.id)
