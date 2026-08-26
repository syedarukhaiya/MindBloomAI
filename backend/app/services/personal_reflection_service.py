from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.personal_reflection import (
    FutureLetter,
    GratitudeCapsule,
    SmallWin,
    KindnessMessage,
    MemoryGarden,
    ReflectionPrompt,
)
from app.schemas.personal_reflection import (
    FutureLetterCreate,
    GratitudeCapsuleCreate,
    SmallWinCreate,
    KindnessMessageCreate,
)


class PersonalReflectionService:
    # Future Letter methods
    @staticmethod
    def create_future_letter(
        db: Session, letter_data: FutureLetterCreate, user_id: int
    ) -> FutureLetter:
        letter = FutureLetter(
            user_id=user_id,
            content=letter_data.content,
            recipient=letter_data.recipient,
            scheduled_for=letter_data.scheduled_for,
        )
        db.add(letter)
        db.commit()
        db.refresh(letter)
        return letter

    @staticmethod
    def get_future_letters(db: Session, user_id: int) -> list[FutureLetter]:
        return db.execute(
            select(FutureLetter).where(FutureLetter.user_id == user_id)
        ).scalars().all()

    @staticmethod
    def get_future_letter(db: Session, letter_id: int, user_id: int) -> FutureLetter | None:
        return db.execute(
            select(FutureLetter).where(
                FutureLetter.id == letter_id, FutureLetter.user_id == user_id
            )
        ).scalar()

    @staticmethod
    def delete_future_letter(db: Session, letter_id: int, user_id: int) -> bool:
        letter = PersonalReflectionService.get_future_letter(db, letter_id, user_id)
        if letter:
            db.delete(letter)
            db.commit()
            return True
        return False

    # Gratitude Capsule methods
    @staticmethod
    def create_gratitude_capsule(
        db: Session, capsule_data: GratitudeCapsuleCreate, user_id: int
    ) -> GratitudeCapsule:
        capsule = GratitudeCapsule(
            user_id=user_id,
            title=capsule_data.title,
            content=capsule_data.content,
            media_url=capsule_data.media_url,
        )
        db.add(capsule)
        db.commit()
        db.refresh(capsule)
        return capsule

    @staticmethod
    def get_gratitude_capsules(db: Session, user_id: int) -> list[GratitudeCapsule]:
        return db.execute(
            select(GratitudeCapsule).where(GratitudeCapsule.user_id == user_id)
        ).scalars().all()

    @staticmethod
    def get_gratitude_capsule(
        db: Session, capsule_id: int, user_id: int
    ) -> GratitudeCapsule | None:
        return db.execute(
            select(GratitudeCapsule).where(
                GratitudeCapsule.id == capsule_id, GratitudeCapsule.user_id == user_id
            )
        ).scalar()

    @staticmethod
    def delete_gratitude_capsule(db: Session, capsule_id: int, user_id: int) -> bool:
        capsule = PersonalReflectionService.get_gratitude_capsule(db, capsule_id, user_id)
        if capsule:
            db.delete(capsule)
            db.commit()
            return True
        return False

    # Small Win methods
    @staticmethod
    def create_small_win(
        db: Session, win_data: SmallWinCreate, user_id: int
    ) -> SmallWin:
        win = SmallWin(
            user_id=user_id,
            content=win_data.content,
            is_anonymous=win_data.is_anonymous,
            visibility=win_data.visibility,
        )
        db.add(win)
        db.commit()
        db.refresh(win)
        return win

    @staticmethod
    def get_small_wins(db: Session, user_id: int) -> list[SmallWin]:
        return db.execute(
            select(SmallWin).where(SmallWin.user_id == user_id)
        ).scalars().all()

    @staticmethod
    def delete_small_win(db: Session, win_id: int, user_id: int) -> bool:
        win = db.execute(
            select(SmallWin).where(SmallWin.id == win_id, SmallWin.user_id == user_id)
        ).scalar()
        if win:
            db.delete(win)
            db.commit()
            return True
        return False

    # Kindness Message methods
    @staticmethod
    def create_kindness_message(
        db: Session, message_data: KindnessMessageCreate, from_user_id: int
    ) -> KindnessMessage:
        message = KindnessMessage(
            from_user_id=from_user_id,
            to_user_id=message_data.to_user_id,
            content=message_data.content,
            is_anonymous=message_data.is_anonymous,
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def get_kindness_messages(db: Session, user_id: int) -> list[KindnessMessage]:
        return db.execute(
            select(KindnessMessage).where(KindnessMessage.to_user_id == user_id)
        ).scalars().all()

    # Memory Garden methods
    @staticmethod
    def get_or_create_memory_garden(db: Session, user_id: int) -> MemoryGarden:
        garden = db.execute(
            select(MemoryGarden).where(MemoryGarden.user_id == user_id)
        ).scalar()
        if not garden:
            garden = MemoryGarden(user_id=user_id)
            db.add(garden)
            db.commit()
            db.refresh(garden)
        return garden

    @staticmethod
    def update_garden_growth(db: Session, user_id: int, bloom_count: int) -> MemoryGarden:
        garden = PersonalReflectionService.get_or_create_memory_garden(db, user_id)
        garden.bloom_count = bloom_count
        # Calculate growth stage (0-5)
        garden.growth_stage = min(5, bloom_count // 10)
        db.commit()
        db.refresh(garden)
        return garden

    # Reflection Prompt methods
    @staticmethod
    def get_reflection_prompts(
        db: Session, category: str | None = None, language: str = "English"
    ) -> list[ReflectionPrompt]:
        query = select(ReflectionPrompt).where(
            ReflectionPrompt.is_active == True,
            ReflectionPrompt.language == language,
        )
        if category:
            query = query.where(ReflectionPrompt.category == category)
        return db.execute(query).scalars().all()
