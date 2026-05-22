from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.permissions import PERMISSOES_PADRAO
from app.infrastructure.postgres.models import Permission, Role


async def seed_roles_and_permissions(session: AsyncSession) -> None:
    for role_name, modules in PERMISSOES_PADRAO.items():
        existing = await session.execute(select(Role).where(Role.name == role_name))
        if existing.scalar_one_or_none():
            continue
        role = Role(name=role_name, description=f"{role_name}")
        session.add(role)
        await session.flush()
        for module, actions in modules.items():
            for action in actions:
                perm = Permission(role_id=role.id, module=module, action=action.value)
                session.add(perm)
    await session.commit()
