from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# Future Letter Schemas
class FutureLetterCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)
    recipient: str = Field(max_length=100, default="My Future Self")
    scheduled_for: datetime


class FutureLetterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    content: str
    recipient: str
    scheduled_for: datetime
    is_sent: bool
    created_at: datetime
    sent_at: datetime | None


# Gratitude Capsule Schemas
class GratitudeCapsuleCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=2000)
    media_url: str | None = None


class GratitudeCapsuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    title: str
    content: str
    media_url: str | None
    created_at: datetime
    updated_at: datetime


# Small Win Schemas
class SmallWinCreate(BaseModel):
    content: str = Field(min_length=1, max_length=1000)
    is_anonymous: bool = True
    visibility: str = Field(pattern="^(PRIVATE|CIRCLE_ONLY|PUBLIC)$", default="PRIVATE")


class SmallWinResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    content: str
    is_anonymous: bool
    visibility: str
    created_at: datetime


# Kindness Message Schemas
class KindnessMessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=1000)
    to_user_id: int | None = None  # None for anonymous drops
    is_anonymous: bool = True


class KindnessMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    from_user_id: int
    to_user_id: int | None
    content: str
    is_anonymous: bool
    created_at: datetime


# Memory Garden Schemas
class MemoryGardenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    bloom_count: int
    growth_stage: int
    last_growth_update: datetime


# Reflection Prompt Schemas
class ReflectionPromptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    category: str
    prompt: str
    language: str
    is_active: bool
