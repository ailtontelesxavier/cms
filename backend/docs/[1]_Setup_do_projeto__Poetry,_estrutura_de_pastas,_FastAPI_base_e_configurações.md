# [1] Setup do projeto: Poetry, estrutura de pastas, FastAPI base e configurações

> **Status:** ✅ Implementado

## Objetivo

Criar o esqueleto do projeto com todas as dependências declaradas, estrutura de pastas da arquitetura hexagonal, configuração via `pydantic-settings` e aplicação FastAPI funcional.

## Tarefas

- [x] Inicializar projeto com Poetry e declarar todas as dependências do SDD (seção 4).
- [x] Criar estrutura de pastas conforme seção 5: `app/core`, `app/middlewares`, `app/domain`, `app/application`, `app/infrastructure`, `app/presentation`, `tests/`.
- [x] Implementar `app/core/config.py` com `Settings` (pydantic-settings, `.env`).
- [x] Implementar `app/core/logging.py` com loguru.
- [x] Implementar `app/core/exceptions.py` com exceções base de domínio.
- [x] Implementar `app/core/pagination.py`.
- [x] Implementar `app/middlewares/request_context.py` e `request_time.py` (request_id, duração, log estruturado, alerta > 1000 ms).
- [x] Criar `app/main.py` montando a aplicação FastAPI com prefixo `/api/v1`, middlewares e router de health.
- [x] Criar `presentation/http/routers/health.py` com endpoint `GET /health`.
- [x] Criar `.env.example` com todas as variáveis necessárias.

## Critérios de Aceite

- `uvicorn app.main:app` inicia sem erros.
- `GET /api/v1/health` retorna `200 OK`.
- Configurações carregam corretamente do `.env`.
- Middleware loga método, path, status e duração de cada requisição.
- Lint (`ruff check .`) passa sem erros.