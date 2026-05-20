from datetime import datetime
from uuid import UUID

from app.application.posts.ports import PostContentRepository, PostRepository
from app.application.posts.schemas import PostCreate, PostOut, PostUpdate
from app.core.pagination import PaginatedParams, PaginatedResult
from app.domain.posts.entities import Post
from app.domain.posts.exceptions import (
    InvalidStatusTransitionError,
    PostContentMissingError,
    PostNotFoundError,
    PostSlugDuplicateError,
)

ALLOWED_TRANSITIONS = {
    "draft": {"review", "archived"},
    "review": {"published", "draft"},
    "published": {"archived"},
    "archived": set(),
}


class PostUseCases:
    def __init__(self, post_repo: PostRepository, content_repo: PostContentRepository) -> None:
        self.post_repo = post_repo
        self.content_repo = content_repo

    async def create(self, data: PostCreate, author_id: UUID) -> PostOut:
        existing = await self.post_repo.get_by_slug(data.slug)
        if existing:
            raise PostSlugDuplicateError(data.slug)

        mongo_id = await self.content_repo.create(
            post_ref_id="",
            html=data.html,
            summary=data.summary,
        )

        now = datetime.utcnow()
        post = Post(
            title=data.title,
            slug=data.slug,
            author_id=author_id,
            mongo_object_id=str(mongo_id),
            status="draft",
            created_at=now,
            updated_at=now,
            tag_ids=data.tag_ids,
        )

        try:
            created = await self.post_repo.create(post)
            await self.content_repo.update(
                str(mongo_id),
                {"post_ref_id": str(created.id)},
            )
        except Exception:
            await self.content_repo.delete(str(mongo_id))
            raise

        return PostOut.model_validate(created)

    async def get_by_id(self, post_id: UUID) -> PostOut:
        post = await self.post_repo.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))
        return PostOut.model_validate(post)

    async def get_by_slug(self, slug: str) -> PostOut:
        post = await self.post_repo.get_by_slug(slug)
        if not post:
            raise PostNotFoundError(slug)
        return PostOut.model_validate(post)

    async def list_all(self, params: PaginatedParams, status: str | None = None) -> PaginatedResult[PostOut]:
        posts = await self.post_repo.list_all(
            skip=params.offset, limit=params.limit, status=status
        )
        total = await self.post_repo.count_all(status=status)
        items = [PostOut.model_validate(p) for p in posts]
        return PaginatedResult.create(items, total, params)

    async def update(self, post_id: UUID, data: PostUpdate) -> PostOut:
        post = await self.post_repo.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))

        if data.title is not None:
            post.title = data.title
        if data.tag_ids is not None:
            post.tag_ids = data.tag_ids

        if data.html is not None:
            await self.content_repo.update(
                post.mongo_object_id,
                {"html": data.html, "summary": data.summary or ""},
            )

        post.updated_at = datetime.utcnow()
        updated = await self.post_repo.update(post)
        return PostOut.model_validate(updated)

    async def publish(self, post_id: UUID) -> PostOut:
        post = await self.post_repo.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))
        if post.status not in ALLOWED_TRANSITIONS or "published" not in ALLOWED_TRANSITIONS[post.status]:
            raise InvalidStatusTransitionError(post.status, "published")

        content = await self.content_repo.get(post.mongo_object_id)
        if not content or not content.get("html"):
            raise PostContentMissingError()

        post.status = "published"
        post.published_at = datetime.utcnow()
        post.updated_at = datetime.utcnow()
        updated = await self.post_repo.update(post)
        return PostOut.model_validate(updated)

    async def archive(self, post_id: UUID) -> PostOut:
        post = await self.post_repo.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))
        if post.status not in ALLOWED_TRANSITIONS or "archived" not in ALLOWED_TRANSITIONS[post.status]:
            raise InvalidStatusTransitionError(post.status, "archived")

        post.status = "archived"
        post.updated_at = datetime.utcnow()
        updated = await self.post_repo.update(post)
        return PostOut.model_validate(updated)

    async def delete(self, post_id: UUID) -> None:
        post = await self.post_repo.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))
        await self.content_repo.delete(post.mongo_object_id)
        await self.post_repo.delete(post)
