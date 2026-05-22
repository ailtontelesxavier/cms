from sqlalchemy import delete as sa_delete, select
from sqlalchemy.orm import selectinload

from app.domain.auth.entities import Role as RoleEntity
from app.infrastructure.postgres.database import Base
from app.infrastructure.postgres.models import Permission, Role


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

    async def get_by_id(self, role_id: int) -> Role | None:
        stmt = select(Role).options(selectinload(Role.permissions)).where(Role.id == role_id)
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def update(self, role: Role) -> Role:
        self.session.add(role)
        await self.session.flush()
        return role

    async def delete(self, role: Role) -> None:
        await self.session.delete(role)
        await self.session.flush()

    async def replace_permissions(self, role_id: int, permissions: list[tuple[str, str]]) -> list[Permission]:
        await self.session.execute(
            sa_delete(Permission).where(Permission.role_id == role_id)
        )
        models = []
        for module, action in permissions:
            perm = Permission(role_id=role_id, module=module, action=action)
            self.session.add(perm)
            models.append(perm)
        await self.session.flush()
        return models
