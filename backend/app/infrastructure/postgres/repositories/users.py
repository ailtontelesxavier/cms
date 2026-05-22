from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.orm import selectinload

from app.domain.auth.entities import User as UserEntity
from app.infrastructure.postgres.database import Base
from app.infrastructure.postgres.models import User


class UserRepository:
    def __init__(self, session: Base) -> None:
        self.session = session

    async def create(self, user: UserEntity) -> User:
        model = User(
            email=user.email,
            name=user.name,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            mfa_enabled=user.mfa_enabled,
            totp_secret=user.totp_secret,
            id=user.id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self.session.add(model)
        await self.session.flush()
        stmt = select(User).options(selectinload(User.roles)).where(User.id == model.id)
        result = await self.session.execute(stmt)
        return result.unique().scalar_one()

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).options(selectinload(User.roles)).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).options(selectinload(User.roles)).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 20, q: str | None = None) -> list[User]:
        stmt = select(User).options(selectinload(User.roles))
        if q:
            stmt = stmt.where(
                or_(User.name.ilike(f'%{q}%'), User.email.ilike(f'%{q}%'))
            )
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.unique().scalars().all())

    async def count_all(self, q: str | None = None) -> int:
        stmt = select(func.count(User.id))
        if q:
            stmt = stmt.where(
                or_(User.name.ilike(f'%{q}%'), User.email.ilike(f'%{q}%'))
            )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def update(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.flush()
