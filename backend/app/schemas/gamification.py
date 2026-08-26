from pydantic import BaseModel


class GamificationResponse(BaseModel):
    user_id: int
    points: int
    level: int
    current_streak: int
    longest_streak: int
    last_activity_date: str | None


class AddPointsRequest(BaseModel):
    points: int


class AchievementResponse(BaseModel):
    id: int
    code: str
    name: str
    description: str
    points_required: int


class GamificationDashboardResponse(BaseModel):
    profile: GamificationResponse
    achievements: list[AchievementResponse]
