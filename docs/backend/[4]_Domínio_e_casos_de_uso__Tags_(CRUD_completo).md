# [4] Domínio e casos de uso: Tags (CRUD completo)

> **Status:** ✅ Implementado

## Objetivo

Implementar a camada de domínio e casos de uso para Tags, com endpoints HTTP protegidos por permissão.

## Tarefas

- [x] Criar entidade `Tag` em `domain/tags/entities.py` com regras: `name` obrigatório, `slug` único, tags inativas não associáveis.
- [x] Criar exceções de domínio em `domain/tags/exceptions.py`.
- [x] Implementar casos de uso em `application/tags/use_cases.py`: criar, listar, buscar por id, atualizar, excluir.
- [x] Implementar schemas Pydantic em `application/tags/schemas.py`.
- [x] Implementar router em `presentation/http/routers/tags.py` com os 5 endpoints (seção 12).
- [x] Proteger endpoints com `require_permission(Modulo.TAGS, Acao.*)`.

## Critérios de Aceite

- `GET /api/v1/tags` retorna lista paginada.
- `POST /api/v1/tags` cria tag e rejeita slug duplicado (409).
- `PATCH /api/v1/tags/{id}` atualiza campos permitidos.
- `DELETE /api/v1/tags/{id}` remove ou desativa tag.
- Usuário sem permissão recebe HTTP 403.
- Testes unitários de domínio e integração HTTP passam.