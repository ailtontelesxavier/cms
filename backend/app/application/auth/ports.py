from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.auth.entities import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 20) -> list[User]: ...

    @abstractmethod
    async def count_all(self) -> int: ...

    @abstractmethod
    async def update(self, user: User) -> User: ...

    @abstractmethod
    async def delete(self, user: User) -> None: ...
