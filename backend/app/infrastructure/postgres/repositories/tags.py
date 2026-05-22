from sqlalchemy import func, select

from app.domain.tags.entities import Tag as TagEntity
from app.infrastructure.postgres.database import Base
from app.infrastructure.postgres.models import Tag


class TagRepository:
    def __init__(self, session: Base) -> None:
        self.session = session

    async def create(self, tag: TagEntity) -> Tag:
        model = Tag(
            name=tag.name,
            description=tag.description,
            is_active=tag.is_active,
            id=tag.id,
            created_at=tag.created_at,
            updated_at=tag.updated_at,
        )
        self.session.add(model)
        await self.session.flush()
        return model

    async def get_by_id(self, tag_id: int) -> Tag | None:
        stmt = select(Tag).where(Tag.id == tag_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 20) -> list[Tag]:
        stmt = select(Tag).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count_all(self) -> int:
        stmt = select(func.count(Tag.id))
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def update(self, tag: Tag) -> Tag:
        self.session.add(tag)
        await self.session.flush()
        return tag

    async def delete(self, tag: Tag) -> None:
        await self.session.delete(tag)
        await self.session.flush()
