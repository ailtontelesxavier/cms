"""seed default roles and permissions from PERMISSOES_PADRAO

Revision ID: a1b2c3d4e5f6
Revises: 52608c1bf91c
Create Date: 2026-05-23 08:00:00.000000

"""
from collections.abc import Sequence

from alembic import op
from sqlalchemy import text

revision: str = "a1b2c3d4e5f6"
down_revision: str | Sequence[str] | None = "52608c1bf91c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

PERMISSOES_PADRAO: dict[str, dict[str, list[str]]] = {
    "Administrador": {
        "administrativo": ["criar", "ler", "atualizar", "excluir", "assinar", "administrar", "relatorios"],
        "auth": ["criar", "ler", "atualizar", "excluir", "assinar", "administrar", "relatorios"],
        "posts": ["criar", "ler", "atualizar", "excluir", "assinar", "administrar", "relatorios"],
        "documentos": ["criar", "ler", "atualizar", "excluir", "assinar", "administrar", "relatorios"],
        "processos": ["criar", "ler", "atualizar", "excluir", "assinar", "administrar", "relatorios"],
        "auditoria": ["criar", "ler", "atualizar", "excluir", "assinar", "administrar", "relatorios"],
        "relatorios": ["criar", "ler", "atualizar", "excluir", "assinar", "administrar", "relatorios"],
    },
    "Diretor": {
        "administrativo": ["ler", "atualizar"],
        "auth": ["criar", "ler", "atualizar"],
        "posts": ["ler", "atualizar"],
        "processos": ["criar", "ler", "assinar"],
        "relatorios": ["ler"],
        "documentos": ["criar", "ler", "atualizar", "assinar"],
    },
    "Secretario": {
        "administrativo": ["ler"],
        "auth": ["ler"],
        "posts": ["ler", "atualizar"],
        "processos": ["criar", "ler"],
        "relatorios": ["ler"],
    },
    "Editor": {
        "posts": ["criar", "ler", "atualizar"],
        "processos": ["ler"],
        "relatorios": ["ler"],
    },
    "Usuario": {
        "posts": ["ler"],
        "processos": ["ler"],
        "relatorios": ["criar", "ler"],
    },
}


def upgrade() -> None:
    conn = op.get_bind()
    for role_name, modules in PERMISSOES_PADRAO.items():
        conn.execute(
            text("""
                INSERT INTO roles (name, description, created_at, updated_at)
                VALUES (:name, :desc, NOW(), NOW())
                ON CONFLICT (name) DO NOTHING
            """),
            {"name": role_name, "desc": role_name},
        )

    for role_name, modules in PERMISSOES_PADRAO.items():
        for module, actions in modules.items():
            for action in actions:
                conn.execute(
                    text("""
                        INSERT INTO permissions (role_id, module, action)
                        SELECT r.id, :module, :action
                        FROM roles r WHERE r.name = :role_name
                        ON CONFLICT (role_id, module, action) DO NOTHING
                    """),
                    {"module": module, "action": action, "role_name": role_name},
                )


def downgrade() -> None:
    conn = op.get_bind()
    for role_name in PERMISSOES_PADRAO:
        conn.execute(
            text("DELETE FROM permissions WHERE role_id = (SELECT id FROM roles WHERE name = :name)"),
            {"name": role_name},
        )
        conn.execute(
            text("DELETE FROM roles WHERE name = :name"),
            {"name": role_name},
        )
