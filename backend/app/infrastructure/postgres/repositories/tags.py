from sqlalchemy import func, select

from app.infrastructure.postgres.database import Base
from app.infrastructure.postgres.models import Tag


class TagRepository:
    def __init__(self, session: Base) -> None:
        self.session = session

    async def create(self, tag: Tag) -> Tag:
        self.session.add(tag)
        await self.session.flush()
        return tag

    async def get_by_id(self, tag_id: int) -> Tag | None:
        stmt = select(Tag).where(Tag.id == tag_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Tag | None:
        stmt = select(Tag).where(Tag.slug == slug)
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
