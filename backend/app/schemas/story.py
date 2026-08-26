from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# Story Schemas
class StoryCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)
    category: str = Field(pattern="^(EXPERIENCE|LESSON|VICTORY|RECOVERY|HOPE)$")
    is_anonymous: bool = True


class StoryUpdate(BaseModel):
    content: str | None = None
    category: str | None = None


class StoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int | None  # None when anonymous
    content: str
    category: str
    is_anonymous: bool
    is_featured: bool
    is_approved: bool
    created_at: datetime
    updated_at: datetime
    reaction_count: int = 0
    user_reaction: str | None = None


class StoryListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    content: str
    category: str
    is_anonymous: bool
    is_featured: bool
    created_at: datetime
    reaction_count: int = 0


# Story Reaction Schemas
class StoryReactionCreate(BaseModel):
    reaction_type: str = Field(pattern="^(I_HEAR_YOU|NOT_ALONE|GAVE_HOPE|SENDING_SUPPORT)$")


class StoryReactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    story_id: int
    reaction_type: str
    created_at: datetime


# Story Report Schemas
class StoryReportCreate(BaseModel):
    reason: str = Field(min_length=1, max_length=500)
