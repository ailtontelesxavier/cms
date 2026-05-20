# Frontend Admin — CMS

Painel administrativo em Vue 3 + TypeScript.

## Quick Start

```bash
# Infraestrutura
docker compose up -d postgres mongodb minio redis

# Migrations do backend
cd backend
poetry run alembic upgrade head

# Criar superusuário
poetry run python scripts/create_superuser.py \
  --email admin@cms.com --name Admin --password admin123

# Iniciar backend
poetry run uvicorn app.main:app --reload

# Iniciar frontend
cd frontend && npm install && npm run dev
```

## Stack

| Camada | Tecnologia |
|---|---|
| Framework | Vue 3 (Composition API) |
| Build | Vite |
| Roteamento | vue-router 4 |
| Estado | Pinia |
| HTTP | Axios |
| Estilos | Tailwind CSS v4 |
| Testes | Vitest + @vue/test-utils |

## Estrutura

```
frontend/
  src/
    app-shell/               # Layout, roteamento
    auth-session/            # Login, MFA, sessão
    content-management/      # Tags, Posts, Imagens
    shared/                  # API client, tipos, UI
```

## Endpoints Consumidos

Todos em `/api/v1`:
- Auth: `/auth/token`, `/auth/mfa/challenge`, `/auth/refresh`, `/users/me`
- MFA: `/auth/mfa/setup`, `/auth/mfa/verify`
- Tags: CRUD `/tags`
- Posts: CRUD `/posts`, detail `/posts/{id}/detail`, publish/archive
- Images: upload/download/delete `/posts/{id}/images`

## Validação E2E

```bash
# Com backend rodando
cd backend && poetry run python scripts/e2e_validate.py
```

## Testes

```bash
cd frontend
npm run test        # 9 testes (session store)
npm run test:watch  # modo watch
```
