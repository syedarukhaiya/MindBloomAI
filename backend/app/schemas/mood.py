from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class MoodCreate(BaseModel):
    mood: str = Field(min_length=1, max_length=50)
    note: str | None = None


class MoodResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    mood: str
    note: str | None
    created_at: datetime
