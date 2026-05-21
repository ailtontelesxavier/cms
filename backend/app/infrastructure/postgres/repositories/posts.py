from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.domain.posts.entities import Post as PostEntity
from app.infrastructure.postgres.database import Base
from app.infrastructure.postgres.models import Post as PostModel
from app.infrastructure.postgres.models import Tag as TagModel


class PostRepository:
    def __init__(self, session: Base) -> None:
        self.session = session

    async def create(self, post: PostEntity) -> PostModel:
        model = PostModel(
            title=post.title,
            slug=post.slug,
            author_id=post.author_id,
            mongo_object_id=post.mongo_object_id,
            status=post.status,
            id=post.id,
            published_at=post.published_at,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
        if post.tag_ids:
            tags_result = await self.session.execute(
                select(TagModel).where(TagModel.id.in_(post.tag_ids))
            )
            model.tags = list(tags_result.scalars().all())

        self.session.add(model)
        await self.session.flush()

        stmt = (
            select(PostModel)
            .options(selectinload(PostModel.tags))
            .where(PostModel.id == model.id)
        )
        result = await self.session.execute(stmt)
        return result.unique().scalar_one()

    async def get_by_id(self, post_id: UUID) -> PostModel | None:
        stmt = select(PostModel).options(
            selectinload(PostModel.tags), selectinload(PostModel.author)
        ).where(PostModel.id == post_id)
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> PostModel | None:
        stmt = select(PostModel).options(
            selectinload(PostModel.tags), selectinload(PostModel.author)
        ).where(PostModel.slug == slug)
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 20, status: str | None = None) -> list[PostModel]:
        stmt = select(PostModel).options(selectinload(PostModel.tags))
        if status:
            stmt = stmt.where(PostModel.status == status)
        stmt = stmt.order_by(PostModel.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.unique().scalars().all())

    async def count_all(self, status: str | None = None) -> int:
        stmt = select(func.count(PostModel.id))
        if status:
            stmt = stmt.where(PostModel.status == status)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def update(self, post: PostModel) -> PostModel:
        self.session.add(post)
        await self.session.flush()
        return post

    async def delete(self, post: PostModel) -> None:
        await self.session.delete(post)
        await self.session.flush()
