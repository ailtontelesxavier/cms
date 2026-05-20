from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class Post:
    title: str
    slug: str
    author_id: UUID
    mongo_object_id: str = ""
    status: str = "draft"
    id: UUID | None = None
    published_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    tag_ids: list[int] = field(default_factory=list)
