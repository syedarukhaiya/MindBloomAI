from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.wellbeing import MoodInsightResponse
from app.security.dependencies import get_current_user
from app.services.wellbeing_service import analyze_wellbeing


router = APIRouter(
    prefix="/wellbeing",
    tags=["Wellbeing & AI Insights"],
)


@router.get(
    "/insights",
    response_model=MoodInsightResponse,
)
def get_wellbeing_insights(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return analyze_wellbeing(db, current_user.id)
