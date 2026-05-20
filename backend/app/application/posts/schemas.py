from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.application.tags.schemas import TagOut


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    slug: str | None = Field(None, max_length=255)
    html: str = Field(..., min_length=1)
    summary: str = Field(default="", max_length=1000)
    tag_ids: list[int] = Field(default_factory=list)


class PostUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=500)
    html: str | None = None
    summary: str | None = None
    tag_ids: list[int] | None = None


class PostOut(BaseModel):
    id: UUID
    title: str
    slug: str
    status: str
    author_id: UUID
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime
    tags: list[TagOut] = []

    model_config = {"from_attributes": True}


class PostContentOut(BaseModel):
    html: str
    plain_text: str
    summary: str
    cover_image: dict | None
    images: list[dict]


class PostDetailOut(PostOut):
    content: PostContentOut | None = None
