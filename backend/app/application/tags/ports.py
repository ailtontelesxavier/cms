from abc import ABC, abstractmethod

from app.domain.tags.entities import Tag


class TagRepository(ABC):
    @abstractmethod
    async def create(self, tag: Tag) -> Tag: ...

    @abstractmethod
    async def get_by_id(self, tag_id: int) -> Tag | None: ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Tag | None: ...

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 20) -> list[Tag]: ...

    @abstractmethod
    async def count_all(self) -> int: ...

    @abstractmethod
    async def update(self, tag: Tag) -> Tag: ...

    @abstractmethod
    async def delete(self, tag: Tag) -> None: ...
