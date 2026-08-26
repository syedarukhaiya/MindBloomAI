from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.gamification import (
    AddPointsRequest,
    GamificationDashboardResponse,
    GamificationResponse,
)
from app.security.dependencies import get_current_user
from app.services.gamification_service import (
    add_points,
    get_dashboard,
    get_or_create_profile,
)


router = APIRouter(
    prefix="/gamification",
    tags=["Gamification"],
)


# ============================================================
# GET GAMIFICATION PROFILE
# ============================================================


@router.get(
    "/",
    response_model=GamificationResponse,
)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_or_create_profile(
        db,
        current_user.id,
    )


# ============================================================
# ADD GAMIFICATION POINTS
# ============================================================


@router.post(
    "/points",
    response_model=GamificationResponse,
    status_code=status.HTTP_200_OK,
)
def award_points(
    data: AddPointsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return add_points(
        db,
        current_user.id,
        data.points,
    )


# ============================================================
# GAMIFICATION DASHBOARD
# ============================================================


@router.get(
    "/dashboard",
    response_model=GamificationDashboardResponse,
)
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile, achievements = get_dashboard(
        db,
        current_user.id,
    )

    return {
        "profile": profile,
        "achievements": achievements,
    }