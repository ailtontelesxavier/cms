# [7] Upload seguro de imagens com MinIO

> **Status:** ✅ Implementado

## Objetivo

Implementar o fluxo completo de upload, download e exclusão de imagens de posts com armazenamento no MinIO.

## Tarefas

- [x] Implementar `infrastructure/minio/client.py` e `storage.py` com operações `put_object`, `get_presigned_url`, `delete_object`.
- [x] Definir porta abstrata `ObjectStorage` em `application/posts/ports.py`.
- [x] Implementar caso de uso de upload em `application/posts/use_cases.py`: validar MIME real (python-magic), gerar nome seguro (`secrets.token_urlsafe`), salvar em `upload/post/{ObjectId}/{safe_name}`, registrar no MongoDB.
- [x] Implementar router `presentation/http/routers/uploads.py` com endpoints de upload, download e exclusão.
- [x] Aplicar rate limit em upload (30/min).
- [x] Rejeitar tipos não permitidos (apenas `image/jpeg`, `image/png`, `image/webp`).

## Critérios de Aceite

- Upload salva objeto no caminho `upload/post/{ObjectId}/{safe_name}`.
- MIME inválido retorna HTTP 415.
- Nome do arquivo do usuário nunca é usado diretamente.
- Download retorna URL assinada ou stream controlado pela API.
- Exclusão remove objeto do MinIO e atualiza documento MongoDB.
- Testes de integração com MinIO (testcontainers ou mock).