from datetime import datetime
from zoneinfo import ZoneInfo

from app.application.tags.ports import TagRepository
from app.application.tags.schemas import TagCreate, TagOut, TagUpdate
from app.core.pagination import PaginatedParams, PaginatedResult
from app.domain.tags.entities import Tag
from app.domain.tags.exceptions import TagDuplicateError, TagNotFoundError


class TagUseCases:
    def __init__(self, repo: TagRepository) -> None:
        self.repo = repo

    async def create(self, data: TagCreate) -> TagOut:
        existing = await self.repo.get_by_slug(data.slug)
        if existing:
            raise TagDuplicateError(data.slug)
        now = datetime.now(ZoneInfo("America/Sao_Paulo"))
        tag = Tag(
            name=data.name,
            slug=data.slug,
            description=data.description,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        created = await self.repo.create(tag)
        return TagOut.model_validate(created)

    async def get_by_id(self, tag_id: int) -> TagOut:
        tag = await self.repo.get_by_id(tag_id)
        if not tag:
            raise TagNotFoundError(tag_id)
        return TagOut.model_validate(tag)

    async def list_all(self, params: PaginatedParams) -> PaginatedResult[TagOut]:
        tags = await self.repo.list_all(skip=params.offset, limit=params.limit)
        total = await self.repo.count_all()
        items = [TagOut.model_validate(t) for t in tags]
        return PaginatedResult.create(items, total, params)

    async def update(self, tag_id: int, data: TagUpdate) -> TagOut:
        tag = await self.repo.get_by_id(tag_id)
        if not tag:
            raise TagNotFoundError(tag_id)
        if data.name is not None:
            tag.name = data.name
        if data.description is not None:
            tag.description = data.description
        tag.updated_at = datetime.now(ZoneInfo("America/Sao_Paulo"))
        updated = await self.repo.update(tag)
        return TagOut.model_validate(updated)

    async def delete(self, tag_id: int) -> None:
        tag = await self.repo.get_by_id(tag_id)
        if not tag:
            raise TagNotFoundError(tag_id)
        await self.repo.delete(tag)
