from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.models import Permission, Role

ROLES_PERMISSIONS = {
    "Master": {
        "auth": ["criar", "ler", "atualizar", "excluir"],
        "posts": ["criar", "ler", "atualizar", "excluir"],
        "tags": ["criar", "ler", "atualizar", "excluir"],
    },
    "Editor": {
        "posts": ["criar", "ler", "atualizar"],
        "tags": ["criar", "ler", "atualizar"],
    },
    "Externo": {
        "posts": ["ler"],
        "tags": ["ler"],
    },
}


async def seed_roles_and_permissions(session: AsyncSession) -> None:
    for role_name, modules in ROLES_PERMISSIONS.items():
        existing = await session.execute(select(Role).where(Role.name == role_name))
        if existing.scalar_one_or_none():
            continue
        role = Role(name=role_name, description=f"{role_name} role")
        session.add(role)
        await session.flush()
        for module, actions in modules.items():
            for action in actions:
                perm = Permission(role_id=role.id, module=module, action=action)
                session.add(perm)
    await session.commit()
