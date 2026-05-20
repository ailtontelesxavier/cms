# [2] PostgreSQL: modelos, repositórios e migrations (Alembic)

> **Status:** ✅ Implementado

## Objetivo

Configurar a camada PostgreSQL com SQLAlchemy AsyncIO, criar todos os modelos ORM, repositórios e migrations via Alembic.

## Tarefas

- [x] Implementar `infrastructure/postgres/database.py` com engine assíncrono e `get_session`.
- [x] Criar modelos ORM em `infrastructure/postgres/models.py`: `users`, `roles`, `user_roles`, `permissions`, `tags`, `posts`, `post_tags`, `audit_logs`.
- [x] Criar repositórios em `infrastructure/postgres/repositories/`: `users.py`, `posts.py`, `tags.py`, `roles.py`.
- [x] Configurar Alembic (`alembic.ini`, `env.py`) para migrations assíncronas.
- [x] Criar migration inicial com todas as tabelas e índices definidos no SDD (seção 7).
- [x] Criar seed de papéis (`Master`, `Editor`, `Externo`) e permissões padrão (seção 9).

## Diagrama de Entidades

```mermaid
classDiagram
    class User {
        +UUID id
        +str email
        +str hashed_password
        +bool mfa_enabled
        +str totp_secret
    }
    class Role {
        +int id
        +str name
    }
    class Permission {
        +int id
        +str module
        +str action
    }
    class Post {
        +UUID id
        +str mongo_object_id
        +str slug
        +str status
    }
    class Tag {
        +int id
        +str slug
        +bool is_active
    }
    class AuditLog {
        +int id
        +str action
        +str resource_type
        +JSONB metadata
    }
    User "n" -- "n" Role : user_roles
    Role "1" -- "n" Permission
    Post "n" -- "n" Tag : post_tags
    Post "1" -- "n" AuditLog
    User "1" -- "n" Post : author
```

## Critérios de Aceite

- `alembic upgrade head` cria todas as tabelas sem erros.
- Índices em `posts.slug`, `posts.mongo_object_id`, `posts.status`, `posts.published_at` existem.
- Seed popula papéis e permissões padrão.
- Repositórios implementam as portas definidas em `application/*/ports.py`.