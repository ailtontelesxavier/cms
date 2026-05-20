from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from app.domain.posts.entities import Post


class PostRepository(ABC):
    @abstractmethod
    async def create(self, post: Post) -> Post: ...

    @abstractmethod
    async def get_by_id(self, post_id: UUID) -> Post | None: ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Post | None: ...

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 20, status: str | None = None) -> list[Post]: ...

    @abstractmethod
    async def count_all(self, status: str | None = None) -> int: ...

    @abstractmethod
    async def update(self, post: Post) -> Post: ...

    @abstractmethod
    async def delete(self, post: Post) -> None: ...


class PostContentRepository(ABC):
    @abstractmethod
    async def create(self, post_ref_id: str, html: str, plain_text: str = "", summary: str = "") -> str: ...

    @abstractmethod
    async def get(self, object_id: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def get_by_post_ref(self, post_ref_id: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def update(self, object_id: str, data: dict[str, Any]) -> bool: ...

    @abstractmethod
    async def delete(self, object_id: str) -> bool: ...

    @abstractmethod
    async def add_image(self, object_id: str, image: dict[str, Any]) -> bool: ...

    @abstractmethod
    async def remove_image(self, object_id: str, object_key: str) -> bool: ...


class ObjectStorage(ABC):
    @abstractmethod
    async def put_object(self, key: str, data: bytes, content_type: str) -> str: ...

    @abstractmethod
    async def get_presigned_url(self, key: str) -> str: ...

    @abstractmethod
    async def delete_object(self, key: str) -> None: ...
