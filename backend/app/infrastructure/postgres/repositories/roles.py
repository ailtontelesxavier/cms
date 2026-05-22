from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.domain.auth.entities import Role as RoleEntity
from app.infrastructure.postgres.database import Base
from app.infrastructure.postgres.models import Role


class RoleRepository:
    def __init__(self, session: Base) -> None:
        self.session = session

    async def get_by_name(self, name: str) -> Role | None:
        stmt = select(Role).options(selectinload(Role.permissions)).where(Role.name == name)
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def list_all(self) -> list[Role]:
        stmt = select(Role).options(selectinload(Role.permissions))
        result = await self.session.execute(stmt)
        return list(result.unique().scalars().all())

    async def create(self, role: RoleEntity) -> Role:
        model = Role(
            name=role.name,
            description=role.description,
            id=role.id,
        )
        self.session.add(model)
        await self.session.flush()
        return model
