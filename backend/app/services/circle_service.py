from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.circle import (
    Circle,
    CircleMembership,
    CircleGathering,
    CircleMessage,
    CircleReaction,
    CircleReport,
)
from app.models.user import User
from app.schemas.circle import CircleCreate, GatheringCreate


class CircleService:
    @staticmethod
    def create_circle(db: Session, circle_data: CircleCreate, creator_id: int) -> Circle:
        circle = Circle(
            name=circle_data.name,
            description=circle_data.description,
            topic=circle_data.topic,
            created_by_user_id=creator_id,
            max_participants=circle_data.max_participants,
        )
        db.add(circle)
        db.commit()
        db.refresh(circle)

        # Add creator as member
        membership = CircleMembership(circle_id=circle.id, user_id=creator_id)
        db.add(membership)
        db.commit()

        return circle

    @staticmethod
    def get_circles(db: Session, skip: int = 0, limit: int = 50) -> list[Circle]:
        return db.execute(
            select(Circle).where(Circle.is_active == True).offset(skip).limit(limit)
        ).scalars().all()

    @staticmethod
    def get_circle(db: Session, circle_id: int) -> Circle | None:
        return db.get(Circle, circle_id)

    @staticmethod
    def join_circle(db: Session, circle_id: int, user_id: int) -> CircleMembership:
        # Check if already a member
        existing = db.execute(
            select(CircleMembership).where(
                CircleMembership.circle_id == circle_id,
                CircleMembership.user_id == user_id,
            )
        ).scalar()
        if existing:
            return existing

        # Check member limit
        circle = db.get(Circle, circle_id)
        member_count = db.execute(
            select(CircleMembership).where(CircleMembership.circle_id == circle_id)
        ).scalars().all()
        
        if len(member_count) >= circle.max_participants:
            raise ValueError("Circle is full")

        membership = CircleMembership(circle_id=circle_id, user_id=user_id)
        db.add(membership)
        db.commit()
        db.refresh(membership)
        return membership

    @staticmethod
    def leave_circle(db: Session, circle_id: int, user_id: int) -> bool:
        membership = db.execute(
            select(CircleMembership).where(
                CircleMembership.circle_id == circle_id,
                CircleMembership.user_id == user_id,
            )
        ).scalar()
        if membership:
            db.delete(membership)
            db.commit()
            return True
        return False

    @staticmethod
    def get_user_circles(db: Session, user_id: int) -> list[Circle]:
        memberships = db.execute(
            select(CircleMembership).where(CircleMembership.user_id == user_id)
        ).scalars().all()
        circle_ids = [m.circle_id for m in memberships]
        if not circle_ids:
            return []
        return db.execute(
            select(Circle).where(Circle.id.in_(circle_ids))
        ).scalars().all()

    @staticmethod
    def create_gathering(
        db: Session, circle_id: int, gathering_data: GatheringCreate
    ) -> CircleGathering:
        gathering = CircleGathering(
            circle_id=circle_id,
            title=gathering_data.title,
            description=gathering_data.description,
            discussion_prompt=gathering_data.discussion_prompt,
            scheduled_at=gathering_data.scheduled_at,
        )
        db.add(gathering)
        db.commit()
        db.refresh(gathering)
        return gathering

    @staticmethod
    def add_message(
        db: Session, gathering_id: int, user_id: int, content: str
    ) -> CircleMessage:
        message = CircleMessage(
            gathering_id=gathering_id, user_id=user_id, content=content
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def add_reaction(
        db: Session, message_id: int, user_id: int, reaction_type: str
    ) -> CircleReaction:
        reaction = CircleReaction(
            message_id=message_id, user_id=user_id, reaction_type=reaction_type
        )
        db.add(reaction)
        db.commit()
        db.refresh(reaction)
        return reaction

    @staticmethod
    def report_message(
        db: Session, message_id: int, reported_by_user_id: int, reason: str
    ) -> CircleReport:
        report = CircleReport(
            message_id=message_id, reported_by_user_id=reported_by_user_id, reason=reason
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def get_circle_members(db: Session, circle_id: int) -> list[User]:
        memberships = db.execute(
            select(CircleMembership).where(CircleMembership.circle_id == circle_id)
        ).scalars().all()
        user_ids = [m.user_id for m in memberships]
        if not user_ids:
            return []
        return db.execute(
            select(User).where(User.id.in_(user_ids))
        ).scalars().all()
