from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class DiaryCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    mood: str | None = Field(default=None, max_length=50)


class DiaryUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)
    mood: str | None = Field(default=None, max_length=50)


class DiaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    content: str
    mood: str | None
    created_at: datetime
    updated_at: datetime
