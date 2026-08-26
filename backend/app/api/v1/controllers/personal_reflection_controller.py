from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.security.dependencies import get_current_user
from app.services.personal_reflection_service import PersonalReflectionService
from app.schemas.personal_reflection import (
    FutureLetterCreate,
    FutureLetterResponse,
    GratitudeCapsuleCreate,
    GratitudeCapsuleResponse,
    SmallWinCreate,
    SmallWinResponse,
    KindnessMessageCreate,
    KindnessMessageResponse,
    MemoryGardenResponse,
    ReflectionPromptResponse,
)

router = APIRouter(tags=["personal_reflection"])


# Future Letter endpoints
@router.post("/future-letters", response_model=FutureLetterResponse)
def create_future_letter(
    letter_data: FutureLetterCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a letter to your future self"""
    letter = PersonalReflectionService.create_future_letter(db, letter_data, current_user.id)
    return FutureLetterResponse.model_validate(letter)


@router.get("/future-letters", response_model=list[FutureLetterResponse])
def get_future_letters(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all your future letters"""
    letters = PersonalReflectionService.get_future_letters(db, current_user.id)
    return [FutureLetterResponse.model_validate(l) for l in letters]


@router.get("/future-letters/{letter_id}", response_model=FutureLetterResponse)
def get_future_letter(
    letter_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific future letter"""
    letter = PersonalReflectionService.get_future_letter(db, letter_id, current_user.id)
    if not letter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return FutureLetterResponse.model_validate(letter)


@router.delete("/future-letters/{letter_id}")
def delete_future_letter(
    letter_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a future letter"""
    if not PersonalReflectionService.delete_future_letter(db, letter_id, current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return {"message": "Letter deleted"}


# Gratitude Capsule endpoints
@router.post("/gratitude-capsules", response_model=GratitudeCapsuleResponse)
def create_gratitude_capsule(
    capsule_data: GratitudeCapsuleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a gratitude capsule to revisit later"""
    capsule = PersonalReflectionService.create_gratitude_capsule(
        db, capsule_data, current_user.id
    )
    return GratitudeCapsuleResponse.model_validate(capsule)


@router.get("/gratitude-capsules", response_model=list[GratitudeCapsuleResponse])
def get_gratitude_capsules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all your gratitude capsules"""
    capsules = PersonalReflectionService.get_gratitude_capsules(db, current_user.id)
    return [GratitudeCapsuleResponse.model_validate(c) for c in capsules]


@router.get("/gratitude-capsules/{capsule_id}", response_model=GratitudeCapsuleResponse)
def get_gratitude_capsule(
    capsule_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific gratitude capsule"""
    capsule = PersonalReflectionService.get_gratitude_capsule(
        db, capsule_id, current_user.id
    )
    if not capsule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return GratitudeCapsuleResponse.model_validate(capsule)


@router.delete("/gratitude-capsules/{capsule_id}")
def delete_gratitude_capsule(
    capsule_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a gratitude capsule"""
    if not PersonalReflectionService.delete_gratitude_capsule(db, capsule_id, current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return {"message": "Capsule deleted"}


# Small Win endpoints
@router.post("/small-wins", response_model=SmallWinResponse)
def create_small_win(
    win_data: SmallWinCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Share a small win"""
    win = PersonalReflectionService.create_small_win(db, win_data, current_user.id)
    return SmallWinResponse.model_validate(win)


@router.get("/small-wins", response_model=list[SmallWinResponse])
def get_small_wins(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all your small wins"""
    wins = PersonalReflectionService.get_small_wins(db, current_user.id)
    return [SmallWinResponse.model_validate(w) for w in wins]


@router.delete("/small-wins/{win_id}")
def delete_small_win(
    win_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a small win"""
    if not PersonalReflectionService.delete_small_win(db, win_id, current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return {"message": "Small win deleted"}


# Kindness Message endpoints
@router.post("/kindness-messages", response_model=KindnessMessageResponse)
def create_kindness_message(
    message_data: KindnessMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Send a kindness message"""
    message = PersonalReflectionService.create_kindness_message(
        db, message_data, current_user.id
    )
    return KindnessMessageResponse.model_validate(message)


@router.get("/kindness-messages", response_model=list[KindnessMessageResponse])
def get_kindness_messages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get kindness messages sent to you"""
    messages = PersonalReflectionService.get_kindness_messages(db, current_user.id)
    return [KindnessMessageResponse.model_validate(m) for m in messages]


# Memory Garden endpoints
@router.get("/garden", response_model=MemoryGardenResponse)
def get_memory_garden(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get your memory garden progress"""
    garden = PersonalReflectionService.get_or_create_memory_garden(db, current_user.id)
    return MemoryGardenResponse.model_validate(garden)


# Reflection Prompt endpoints
@router.get("/reflection-prompts", response_model=list[ReflectionPromptResponse])
def get_reflection_prompts(
    category: str | None = None,
    language: str = "English",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get reflection prompts"""
    prompts = PersonalReflectionService.get_reflection_prompts(
        db, category, language
    )
    return [ReflectionPromptResponse.model_validate(p) for p in prompts]
