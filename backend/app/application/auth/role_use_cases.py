from uuid import UUID

from app.application.auth.schemas import (
    PermissionOut,
    RoleCreate,
    RoleOut,
    RolePermissionUpdate,
    RoleUpdate,
    UserRoleAssign,
)
from app.domain.auth.entities import Role as RoleEntity
from app.domain.auth.exceptions import PermissionDeniedError
from app.infrastructure.postgres.repositories.roles import RoleRepository
from app.infrastructure.postgres.repositories.users import UserRepository


class RoleUseCases:
    def __init__(self, role_repo: RoleRepository, user_repo: UserRepository) -> None:
        self.role_repo = role_repo
        self.user_repo = user_repo

    async def list_roles(self) -> list[RoleOut]:
        roles = await self.role_repo.list_all()
        return [self._to_role_out(r) for r in roles]

    async def get_role(self, role_id: int) -> RoleOut:
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            raise PermissionDeniedError("role", str(role_id))
        return self._to_role_out(role)

    async def create_role(self, data: RoleCreate) -> RoleOut:
        now = None
        role = RoleEntity(name=data.name, description=data.description)
        created = await self.role_repo.create(role)
        created = await self.role_repo.get_by_id(created.id)
        return self._to_role_out(created)

    async def update_role(self, role_id: int, data: RoleUpdate) -> RoleOut:
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            raise PermissionDeniedError("role", str(role_id))
        if data.name is not None:
            role.name = data.name
        if data.description is not None:
            role.description = data.description
        updated = await self.role_repo.update(role)
        return self._to_role_out(updated)

    async def update_role_permissions(self, role_id: int, data: RolePermissionUpdate) -> RoleOut:
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            raise PermissionDeniedError("role", str(role_id))
        perms = [(p.module.value, p.action.value) for p in data.permissions]
        await self.role_repo.replace_permissions(role_id, perms)
        updated = await self.role_repo.get_by_id(role_id)
        return self._to_role_out(updated)

    async def delete_role(self, role_id: int) -> None:
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            raise PermissionDeniedError("role", str(role_id))
        await self.role_repo.delete(role)

    async def assign_roles_to_user(self, user_id: UUID, data: UserRoleAssign) -> None:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise PermissionDeniedError("users", str(user_id))
        await self.user_repo.assign_roles(user, data.role_ids)

    def _to_role_out(self, role) -> RoleOut:
        return RoleOut(
            id=role.id,
            name=role.name,
            description=role.description,
            permissions=[
                PermissionOut(id=p.id, module=p.module, action=p.action)
                for p in role.permissions
            ],
        )
