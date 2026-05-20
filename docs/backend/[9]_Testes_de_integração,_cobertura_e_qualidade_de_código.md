# [9] Testes de integração, cobertura e qualidade de código

> **Status:** ⚠️ Parcial (código implementado, testes incompletos)

## Objetivo

Garantir cobertura mínima de 80%, com fixtures assíncronas, factories e testes obrigatórios definidos no SDD.

## Tarefas

- [ ] ~~Implementar `tests/conftest.py` com fixtures PostgreSQL (testcontainers), sessão assíncrona, client HTTP e `mock_db_time`.~~ ⚠️ **Pendente** — `conftest.py` atual tem apenas fixtures mínimas (`mock_db_time` vazia, `anyio_backend`). Sem testcontainers.
- [x] Criar factories em `tests/factories/`: `UserFactory`, `PostFactory`, `TagFactory`.
- [x] Implementar testes unitários em `tests/unit/domain/` (`test_posts.py`, `test_tags.py`).
- [ ] ~~Implementar testes unitários em `tests/unit/application/`.~~ ❌ **Pendente** — diretório vazio.
- [ ] ~~Implementar testes de integração em `tests/integration/http/`, `postgres/`, `mongodb/`, `minio/`.~~ ⚠️ **Parcial** — apenas `test_health.py` e `test_tags.py` (básicos, sem DB). `postgres/`, `mongodb/`, `minio/` vazios.
- [ ] ~~Cobrir todos os casos obrigatórios da seção 21 do SDD.~~ ❌ **Pendente** — nenhum dos 9 casos obrigatórios está completamente implementado.
- [x] Configurar `pyproject.toml` com `asyncio_mode = auto` e `testpaths`.
- [ ] ~~Garantir que `ruff check .` e `typos` passam sem erros.~~ ❌ **Pendente** — verificação necessária.

## Critérios de Aceite

- `pytest --cov=app --cov-report=term-missing` reporta ≥ 80% de cobertura.
- Todos os 11 casos de teste obrigatórios do SDD passam.
- `ruff check .` sem erros.
- `typos` sem erros.
- CI pode executar a suite completa com `docker` disponível (testcontainers).