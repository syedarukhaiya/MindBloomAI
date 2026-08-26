from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.security.dependencies import get_current_user
from app.services.story_service import StoryService
from app.schemas.story import (
    StoryCreate,
    StoryResponse,
    StoryListResponse,
    StoryReactionCreate,
    StoryReportCreate,
)

router = APIRouter(prefix="/stories", tags=["stories"])


@router.post("", response_model=StoryResponse)
def create_story(
    story_data: StoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create and share an anonymous story in the Story Garden"""
    story = StoryService.create_story(db, story_data, current_user.id)
    reactions = StoryService.get_story_reactions(db, story.id)
    response = StoryResponse.model_validate(story)
    response.reaction_count = sum(reactions.values())
    response.user_reaction = StoryService.get_user_reaction(db, story.id, current_user.id)
    return response


@router.get("", response_model=list[StoryListResponse])
def list_stories(
    skip: int = 0,
    limit: int = 50,
    category: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all approved stories from the Story Garden"""
    stories = StoryService.get_stories(db, skip, limit, category)
    result = []
    for story in stories:
        reactions = StoryService.get_story_reactions(db, story.id)
        result.append(
            StoryListResponse(
                id=story.id,
                content=story.content,
                category=story.category,
                is_anonymous=story.is_anonymous,
                is_featured=story.is_featured,
                created_at=story.created_at,
                reaction_count=sum(reactions.values()),
            )
        )
    return result


@router.get("/featured", response_model=list[StoryListResponse])
def get_featured_stories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get featured stories"""
    stories = StoryService.get_featured_stories(db)
    result = []
    for story in stories:
        reactions = StoryService.get_story_reactions(db, story.id)
        result.append(
            StoryListResponse(
                id=story.id,
                content=story.content,
                category=story.category,
                is_anonymous=story.is_anonymous,
                is_featured=story.is_featured,
                created_at=story.created_at,
                reaction_count=sum(reactions.values()),
            )
        )
    return result


@router.get("/{story_id}", response_model=StoryResponse)
def get_story(
    story_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific story"""
    story = StoryService.get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    reactions = StoryService.get_story_reactions(db, story.id)
    response = StoryResponse.model_validate(story)
    response.reaction_count = sum(reactions.values())
    response.user_reaction = StoryService.get_user_reaction(db, story.id, current_user.id)
    return response


@router.delete("/{story_id}")
def delete_story(
    story_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete your own story"""
    story = StoryService.get_story(db, story_id)
    if not story or story.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own stories",
        )
    StoryService.delete_story(db, story_id)
    return {"message": "Story deleted"}


@router.post("/{story_id}/reactions")
def add_reaction(
    story_id: int,
    reaction_data: StoryReactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a reaction to a story"""
    story = StoryService.get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    
    StoryService.add_reaction(db, story_id, current_user.id, reaction_data.reaction_type)
    return {"message": "Reaction added"}


@router.delete("/{story_id}/reactions/{reaction_type}")
def remove_reaction(
    story_id: int,
    reaction_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove a reaction from a story"""
    success = StoryService.remove_reaction(
        db, story_id, current_user.id, reaction_type
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reaction not found"
        )
    return {"message": "Reaction removed"}


@router.post("/{story_id}/report")
def report_story(
    story_id: int,
    report_data: StoryReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Report a story"""
    story = StoryService.get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    
    StoryService.report_story(db, story_id, current_user.id, report_data.reason)
    return {"message": "Story reported"}
