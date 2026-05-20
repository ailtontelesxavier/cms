# [8] Redis, rate limit (slowapi) e jobs assíncronos (ARQ)

> **Status:** ✅ Implementado

## Objetivo

Configurar Redis como backend de rate limit e fila de jobs ARQ para tarefas assíncronas de limpeza e auditoria.

## Tarefas

- [x] Implementar `infrastructure/redis/client.py` e `rate_limit.py`.
- [x] Configurar slowapi com Redis como storage e aplicar políticas por rota (seção 16).
- [x] Implementar `infrastructure/arq/worker.py` e `jobs.py` com jobs: remoção de conteúdos órfãos no MongoDB, remoção de objetos órfãos no MinIO, geração de `plain_text` a partir do HTML.
- [x] Integrar enfileiramento de jobs nos casos de uso de compensação (ticket [5]).

## Critérios de Aceite

- Rate limit em `/auth/token` bloqueia após 5 req/min por IP.
- Worker ARQ inicia e processa jobs da fila Redis.
- Job de limpeza remove documentos MongoDB marcados como órfãos.
- Configuração do worker declarada em `pyproject.toml` ou script dedicado.