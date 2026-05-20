from collections.abc import AsyncGenerator
from uuid import UUID

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.auth.use_cases import AuthUseCases
from app.application.posts.use_cases import PostUseCases
from app.application.tags.use_cases import TagUseCases
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_token
from app.domain.auth.entities import User
from app.infrastructure.mongodb.client import get_mongo_db
from app.infrastructure.mongodb.repositories.post_contents import PostContentRepository
from app.infrastructure.postgres.database import get_session
from app.infrastructure.postgres.repositories.posts import PostRepository
from app.infrastructure.postgres.repositories.tags import TagRepository
from app.infrastructure.postgres.repositories.users import UserRepository


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session


async def get_user_repo(session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(session)


async def get_tag_repo(session: AsyncSession = Depends(get_db_session)) -> TagRepository:
    return TagRepository(session)


async def get_post_repo(session: AsyncSession = Depends(get_db_session)) -> PostRepository:
    return PostRepository(session)


async def get_content_repo() -> PostContentRepository:
    db = await get_mongo_db()
    return PostContentRepository(db)


async def get_auth_use_cases(repo: UserRepository = Depends(get_user_repo)) -> AuthUseCases:
    return AuthUseCases(repo)


async def get_tag_use_cases(repo: TagRepository = Depends(get_tag_repo)) -> TagUseCases:
    return TagUseCases(repo)


async def get_post_use_cases(
    post_repo: PostRepository = Depends(get_post_repo),
    content_repo: PostContentRepository = Depends(get_content_repo),
) -> PostUseCases:
    return PostUseCases(post_repo, content_repo)


async def get_current_user(
    authorization: str = Header(default=""),
    user_repo: UserRepository = Depends(get_user_repo),
) -> User:
    if not authorization.startswith("Bearer "):
        raise UnauthorizedError("Missing or invalid token")
    token = authorization.removeprefix("Bearer ")
    try:
        payload = decode_token(token)
    except Exception:
        raise UnauthorizedError("Invalid token") from None

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Invalid token")

    user = await user_repo.get_by_id(UUID(user_id))
    if not user or not user.is_active:
        raise UnauthorizedError("User not found or inactive")
    return user


class PermissionChecker:
    def __init__(self, module: str, action: str) -> None:
        self.module = module
        self.action = action

    async def __call__(self, user: User = Depends(get_current_user)) -> User:
        if user.is_superuser:
            return user
        for role in user.roles:
            for perm in role.permissions:
                if perm.module == self.module and perm.action == self.action:
                    return user
        raise ForbiddenError(f"Permission denied: {self.module}:{self.action}")


def require_permission(module: str, action: str) -> PermissionChecker:
    return PermissionChecker(module, action)
