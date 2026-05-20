# [3] MongoDB: cliente Motor e repositório de conteúdo de posts

> **Status:** ✅ Implementado

## Objetivo

Configurar a conexão com MongoDB via Motor e implementar o repositório `post_contents` com os índices necessários.

## Tarefas

- [x] Implementar `infrastructure/mongodb/client.py` com inicialização do Motor e injeção via `lifespan` do FastAPI.
- [x] Implementar `infrastructure/mongodb/repositories/post_contents.py` com operações: `create`, `get`, `update`, `delete`.
- [x] Criar índices na coleção `post_contents`: `post_ref_id` e `updated_at`.
- [x] Definir porta abstrata `PostContentRepository` em `application/posts/ports.py`.

## Critérios de Aceite

- Conexão com MongoDB inicializa e fecha corretamente no ciclo de vida da aplicação.
- CRUD de `post_contents` funciona com documentos no formato definido no SDD (seção 7).
- Índices criados na inicialização.