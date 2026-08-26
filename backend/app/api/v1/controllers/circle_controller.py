from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.database import get_db
from app.models.user import User
from app.security.dependencies import get_current_user
from app.services.circle_service import CircleService
from app.schemas.circle import (
    CircleCreate,
    CircleResponse,
    CircleListResponse,
    GatheringCreate,
    GatheringResponse,
    CircleMessageCreate,
    CircleMessageResponse,
    CircleReactionCreate,
    CircleReportCreate,
)

router = APIRouter(prefix="/circles", tags=["circles"])


@router.post("", response_model=CircleResponse)
def create_circle(
    circle_data: CircleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new wellbeing circle"""
    circle = CircleService.create_circle(db, circle_data, current_user.id)
    return CircleResponse.model_validate(circle)


@router.get("", response_model=list[CircleListResponse])
def list_circles(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all active circles"""
    circles = CircleService.get_circles(db, skip, limit)
    return [
        CircleListResponse(
            id=c.id,
            name=c.name,
            topic=c.topic,
            description=c.description,
            member_count=len(CircleService.get_circle_members(db, c.id)),
        )
        for c in circles
    ]


@router.get("/{circle_id}", response_model=CircleResponse)
def get_circle(
    circle_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get circle details"""
    circle = CircleService.get_circle(db, circle_id)
    if not circle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Circle not found")
    members = CircleService.get_circle_members(db, circle_id)
    response = CircleResponse.model_validate(circle)
    response.member_count = len(members)
    return response


@router.post("/{circle_id}/join")
def join_circle(
    circle_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Join a circle"""
    try:
        CircleService.join_circle(db, circle_id, current_user.id)
        return {"message": "Successfully joined circle"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{circle_id}/leave")
def leave_circle(
    circle_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Leave a circle"""
    success = CircleService.leave_circle(db, circle_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not a member of this circle"
        )
    return {"message": "Successfully left circle"}


@router.get("/my-circles", response_model=list[CircleListResponse])
def get_my_circles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get circles the user has joined"""
    circles = CircleService.get_user_circles(db, current_user.id)
    return [
        CircleListResponse(
            id=c.id,
            name=c.name,
            topic=c.topic,
            description=c.description,
            member_count=len(CircleService.get_circle_members(db, c.id)),
        )
        for c in circles
    ]


# Gathering endpoints
@router.post("/{circle_id}/gatherings", response_model=GatheringResponse)
def create_gathering(
    circle_id: int,
    gathering_data: GatheringCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a circle gathering"""
    circle = CircleService.get_circle(db, circle_id)
    if not circle or circle.created_by_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    gathering = CircleService.create_gathering(db, circle_id, gathering_data)
    return GatheringResponse.model_validate(gathering)


# Message endpoints
@router.post("/{circle_id}/gatherings/{gathering_id}/messages", response_model=CircleMessageResponse)
def add_message(
    circle_id: int,
    gathering_id: int,
    message_data: CircleMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add message to a circle gathering"""
    message = CircleService.add_message(
        db, gathering_id, current_user.id, message_data.content
    )
    return CircleMessageResponse.model_validate(message)


@router.post("/{circle_id}/gatherings/{gathering_id}/messages/{message_id}/reactions")
def add_reaction(
    circle_id: int,
    gathering_id: int,
    message_id: int,
    reaction_data: CircleReactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add reaction to a message"""
    CircleService.add_reaction(
        db, message_id, current_user.id, reaction_data.reaction_type
    )
    return {"message": "Reaction added"}


@router.post("/{circle_id}/gatherings/{gathering_id}/messages/{message_id}/report")
def report_message(
    circle_id: int,
    gathering_id: int,
    message_id: int,
    report_data: CircleReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Report a message"""
    CircleService.report_message(
        db, message_id, current_user.id, report_data.reason
    )
    return {"message": "Message reported"}
