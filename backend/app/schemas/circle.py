from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# Circle Schemas
class CircleCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=1000)
    topic: str = Field(min_length=1, max_length=100)
    max_participants: int = Field(25, ge=5, le=100)


class CircleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    topic: str
    created_by_user_id: int
    max_participants: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    member_count: int = 0


class CircleListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    topic: str
    description: str
    member_count: int


# Circle Gathering Schemas
class GatheringCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    discussion_prompt: str | None = None
    scheduled_at: datetime


class GatheringResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    circle_id: int
    title: str
    description: str | None
    discussion_prompt: str | None
    scheduled_at: datetime
    created_at: datetime


# Circle Message Schemas
class CircleMessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)


class CircleMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    gathering_id: int
    user_id: int
    content: str
    created_at: datetime


class CircleReactionCreate(BaseModel):
    reaction_type: str = Field(pattern="^(I_HEAR_YOU|NOT_ALONE|GAVE_HOPE|SENDING_SUPPORT)$")


class CircleReportCreate(BaseModel):
    reason: str = Field(min_length=1, max_length=500)
