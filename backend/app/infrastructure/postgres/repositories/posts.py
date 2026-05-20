from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.infrastructure.postgres.database import Base
from app.infrastructure.postgres.models import Post


class PostRepository:
    def __init__(self, session: Base) -> None:
        self.session = session

    async def create(self, post: Post) -> Post:
        self.session.add(post)
        await self.session.flush()
        return post

    async def get_by_id(self, post_id: UUID) -> Post | None:
        stmt = select(Post).options(
            selectinload(Post.tags), selectinload(Post.author)
        ).where(Post.id == post_id)
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Post | None:
        stmt = select(Post).options(
            selectinload(Post.tags), selectinload(Post.author)
        ).where(Post.slug == slug)
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 20, status: str | None = None) -> list[Post]:
        stmt = select(Post).options(selectinload(Post.tags))
        if status:
            stmt = stmt.where(Post.status == status)
        stmt = stmt.order_by(Post.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.unique().scalars().all())

    async def count_all(self, status: str | None = None) -> int:
        stmt = select(func.count(Post.id))
        if status:
            stmt = stmt.where(Post.status == status)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def update(self, post: Post) -> Post:
        self.session.add(post)
        await self.session.flush()
        return post

    async def delete(self, post: Post) -> None:
        await self.session.delete(post)
        await self.session.flush()
