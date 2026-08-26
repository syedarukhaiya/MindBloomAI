from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.story import Story, StoryReaction, StoryReport
from app.schemas.story import StoryCreate, StoryUpdate


class StoryService:
    @staticmethod
    def create_story(db: Session, story_data: StoryCreate, user_id: int) -> Story:
        story = Story(
            user_id=user_id,
            content=story_data.content,
            category=story_data.category,
            is_anonymous=story_data.is_anonymous,
        )
        db.add(story)
        db.commit()
        db.refresh(story)
        return story

    @staticmethod
    def get_stories(
        db: Session, skip: int = 0, limit: int = 50, category: str | None = None
    ) -> list[Story]:
        query = select(Story).where(Story.is_approved == True)
        if category:
            query = query.where(Story.category == category)
        return db.execute(query.offset(skip).limit(limit)).scalars().all()

    @staticmethod
    def get_featured_stories(db: Session, limit: int = 10) -> list[Story]:
        return db.execute(
            select(Story)
            .where(Story.is_featured == True, Story.is_approved == True)
            .limit(limit)
        ).scalars().all()

    @staticmethod
    def get_story(db: Session, story_id: int) -> Story | None:
        return db.get(Story, story_id)

    @staticmethod
    def update_story(db: Session, story_id: int, story_data: StoryUpdate) -> Story | None:
        story = db.get(Story, story_id)
        if not story:
            return None
        if story_data.content is not None:
            story.content = story_data.content
        if story_data.category is not None:
            story.category = story_data.category
        db.commit()
        db.refresh(story)
        return story

    @staticmethod
    def delete_story(db: Session, story_id: int) -> bool:
        story = db.get(Story, story_id)
        if story:
            db.delete(story)
            db.commit()
            return True
        return False

    @staticmethod
    def get_user_stories(db: Session, user_id: int) -> list[Story]:
        return db.execute(
            select(Story).where(Story.user_id == user_id)
        ).scalars().all()

    @staticmethod
    def add_reaction(
        db: Session, story_id: int, user_id: int, reaction_type: str
    ) -> StoryReaction:
        reaction = StoryReaction(
            story_id=story_id, user_id=user_id, reaction_type=reaction_type
        )
        db.add(reaction)
        db.commit()
        db.refresh(reaction)
        return reaction

    @staticmethod
    def remove_reaction(db: Session, story_id: int, user_id: int, reaction_type: str) -> bool:
        reaction = db.execute(
            select(StoryReaction).where(
                StoryReaction.story_id == story_id,
                StoryReaction.user_id == user_id,
                StoryReaction.reaction_type == reaction_type,
            )
        ).scalar()
        if reaction:
            db.delete(reaction)
            db.commit()
            return True
        return False

    @staticmethod
    def get_story_reactions(db: Session, story_id: int) -> dict[str, int]:
        reactions = db.execute(
            select(StoryReaction.reaction_type, func.count(StoryReaction.id)).where(
                StoryReaction.story_id == story_id
            ).group_by(StoryReaction.reaction_type)
        ).all()
        return {r[0]: r[1] for r in reactions}

    @staticmethod
    def report_story(
        db: Session, story_id: int, reported_by_user_id: int, reason: str
    ) -> StoryReport:
        report = StoryReport(
            story_id=story_id, reported_by_user_id=reported_by_user_id, reason=reason
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def get_user_reaction(
        db: Session, story_id: int, user_id: int
    ) -> str | None:
        reaction = db.execute(
            select(StoryReaction).where(
                StoryReaction.story_id == story_id,
                StoryReaction.user_id == user_id,
            )
        ).scalar()
        return reaction.reaction_type if reaction else None
