# SDD - Backend CMS FastAPI com Arquitetura Hexagonal

## 1. Objetivo

Criar um backend de APIs REST em FastAPI para um CMS consumido por um frontend em Vue.js 3.5.

O sistema deve usar arquitetura hexagonal, separar regras de negocio de detalhes de infraestrutura e persistir dados em dois bancos:

- PostgreSQL: usuarios, autenticacao, autorizacao, referencias de posts, tags e demais dados transacionais.
- MongoDB: conteudo completo das materias, incluindo HTML e metadados editoriais volumosos.

As imagens dos posts devem ser vinculadas ao `ObjectId` do documento no MongoDB e armazenadas em object storage MinIO, com caminho logico `upload/post/{ObjectId}`.

## 2. Escopo

Este SDD cobre:

- Estrutura do projeto backend em FastAPI.
- Organizacao por arquitetura hexagonal.
- Modelo de dados PostgreSQL e MongoDB.
- Fluxos de cadastro, edicao, publicacao e consulta de posts.
- Cadastro e uso de tags.
- Autenticacao, autorizacao e permissoes por modulo.
- Upload seguro de arquivos e integracao com MinIO.
- Middlewares, logs, rate limit e tratamento de erros.
- Dependencias Poetry.
- Estrategia de testes com Pytest, Testcontainers e fixtures assincronas.
- Pontos de integracao com Vue.js 3.5.

Fora do escopo inicial:

- Implementacao completa do frontend.
- Workflow editorial avancado com revisores multiplos.
- Busca full-text distribuida.
- CDN publica para imagens.

## 3. Stack Tecnica

### Backend

- Python 3.12+
- FastAPI
- Uvicorn
- Pydantic v2
- Pydantic Settings
- SQLAlchemy AsyncIO
- Alembic
- asyncpg
- Motor
- Redis 7.4
- ARQ para jobs assincronos
- MinIO como object store S3-compatible
- fastapi-users ou camada propria de autenticacao baseada em JWT
- PyJWT
- pwdlib[argon2]
- pyotp e qrcode[pil] para MFA/TOTP
- slowapi para rate limit
- python-magic para validacao real de MIME type
- python-multipart para uploads
- loguru para logs estruturados
- validate-docbr para documentos brasileiros

### Frontend

- Vue.js 3.5
- Editorjs
- `file-type` para validacao auxiliar do tipo real de arquivo antes do upload

### Qualidade e Testes

- pytest
- pytest-asyncio
- pytest-cov
- testcontainers
- factory-boy
- freezegun
- ruff
- typos

## 4. Dependencias Poetry

Exemplo inicial de dependencias:

```toml
[tool.poetry.dependencies]
python = "^3.12"
fastapi = {extras = ["standard"], version = "^0.115.0"}
uvicorn = "^0.34.0"
pydantic = {extras = ["email"], version = "^2.11.10"}
pydantic-settings = "^2.7.0"
pydantic-extra-types = "^2.10.0"
sqlalchemy = {extras = ["asyncio"], version = "^2.0.0"}
asyncpg = "^0.30.0"
alembic = "^1.14.0"
motor = "^3.6.0"
redis = "^7.4.0"
arq = "^0.26.0"
pyjwt = "^2.10.0"
pwdlib = {extras = ["argon2"], version = "^0.2.0"}
fastapi-users = "^14.0.0"
slowapi = "^0.1.9"
python-magic = "^0.4.27"
python-multipart = "^0.0.20"
python-dotenv = "^1.0.1"
loguru = "^0.7.3"
validate-docbr = "^1.10.0"
pyotp = "^2.9.0"
qrcode = {extras = ["pil"], version = "^8.2"}
httpx = "^0.28.0"
minio = "^7.2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.3.0"
pytest-asyncio = "^0.25.0"
pytest-cov = "^6.0.0"
testcontainers = "^4.9.0"
factory-boy = "^3.3.0"
freezegun = "^1.5.0"
ruff = "^0.8.0"
typos = "^1.28.0"
poetry-shell = "^1.0.0"
```

Observacao: se o projeto optar por `fastapi-users`, deve ser validado se o modelo de usuario, MFA e permissoes por modulo se encaixam bem. Caso contrario, a autenticacao deve ser implementada na camada de aplicacao usando `PyJWT` e `pwdlib[argon2]`.

## 5. Arquitetura Hexagonal

O backend deve separar dominio, casos de uso, portas e adaptadores.

Estrutura sugerida:

```text
app/
  main.py
  core/
    config.py
    logging.py
    security.py
    exceptions.py
    pagination.py
  middlewares/
    request_context.py
    request_time.py
  domain/
    auth/
      entities.py
      value_objects.py
      exceptions.py
      permissions.py
    posts/
      entities.py
      value_objects.py
      exceptions.py
    tags/
      entities.py
      exceptions.py
  application/
    auth/
      use_cases.py
      ports.py
      schemas.py
    posts/
      use_cases.py
      ports.py
      schemas.py
    tags/
      use_cases.py
      ports.py
      schemas.py
  infrastructure/
    postgres/
      database.py
      models.py
      repositories/
        users.py
        posts.py
        tags.py
        roles.py
      migrations/
    mongodb/
      client.py
      repositories/
        post_contents.py
    minio/
      client.py
      storage.py
    redis/
      client.py
      rate_limit.py
    arq/
      worker.py
      jobs.py
  presentation/
    http/
      dependencies.py
      error_handlers.py
      routers/
        auth.py
        users.py
        posts.py
        tags.py
        uploads.py
        health.py
tests/
  factories/
  integration/
  unit/
```

### Regras de Dependencia

- `domain` nao importa FastAPI, SQLAlchemy, Motor, MinIO ou Redis.
- `application` conhece entidades de dominio e portas abstratas.
- `infrastructure` implementa portas usando PostgreSQL, MongoDB, MinIO e Redis.
- `presentation` converte HTTP em chamadas de caso de uso.
- `main.py` monta a aplicacao e injeta dependencias.

## 6. Configuracao

Usar `pydantic-settings`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "CMS API"
    environment: str = "local"
    api_prefix: str = "/api/v1"

    postgres_dsn: str
    mongodb_dsn: str
    mongodb_database: str = "cms"

    redis_dsn: str = "redis://localhost:6379/0"

    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str = "cms"
    minio_secure: bool = False

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
```

## 7. Modelo de Dados

### PostgreSQL

O PostgreSQL armazena dados relacionais, referencia do conteudo MongoDB e informacoes necessarias para listagem rapida.

Tabelas principais:

#### users

Campos:

- `id`: UUID ou bigint.
- `email`: unico.
- `name`.
- `hashed_password`.
- `is_active`.
- `is_superuser`.
- `mfa_enabled`.
- `totp_secret`.
- `created_at`.
- `updated_at`.

#### roles

Campos:

- `id`.
- `name`: unico. Exemplo: `Master`, `Editor`.
- `description`.
- `created_at`.
- `updated_at`.

#### user_roles

Campos:

- `user_id`.
- `role_id`.

#### permissions

Campos:

- `id`.
- `role_id`.
- `module`.
- `action`.

Restricao unica:

- `role_id`, `module`, `action`.

#### tags

Campos:

- `id`.
- `name`.
- `slug`: unico.
- `description`.
- `is_active`.
- `created_at`.
- `updated_at`.

#### posts

Campos:

- `id`: UUID ou bigint.
- `mongo_object_id`: string com o `ObjectId` do MongoDB.
- `title`.
- `slug`: unico.
- `status`: `draft`, `review`, `published`, `archived`.
- `author_id`.
- `published_at`.
- `created_at`.
- `updated_at`.

Indices:

- `posts.slug`.
- `posts.mongo_object_id`.
- `posts.status`.
- `posts.published_at`.

#### post_tags

Tabela associativa:

- `post_id`.
- `tag_id`.

Restricao unica:

- `post_id`, `tag_id`.

### MongoDB

Colecao: `post_contents`

Documento:

```json
{
  "_id": "ObjectId",
  "post_ref_id": "uuid-ou-id-postgresql",
  "html": "<h1>Conteudo da materia</h1>",
  "plain_text": "Conteudo da materia",
  "summary": "Resumo opcional",
  "cover_image": {
    "object_key": "upload/post/{ObjectId}/cover_xxxxx.jpg",
    "content_type": "image/jpeg",
    "size": 123456
  },
  "images": [
    {
      "object_key": "upload/post/{ObjectId}/image_xxxxx.png",
      "content_type": "image/png",
      "size": 123456,
      "alt": "Texto alternativo"
    }
  ],
  "created_at": "2026-05-20T00:00:00Z",
  "updated_at": "2026-05-20T00:00:00Z"
}
```

Indices:

- `post_ref_id`.
- `updated_at`.

## 8. Entidades de Dominio

### Post

A entidade `Post` representa a referencia relacional do conteudo.

Regras:

- Todo post deve ter titulo.
- Todo post deve ter slug unico.
- Todo post pode ter zero ou mais tags.
- Tags recebidas no cadastro devem existir ou ser criadas por caso de uso explicito, conforme politica do produto.
- O HTML nao fica no PostgreSQL.
- O `mongo_object_id` deve existir depois da criacao do conteudo no MongoDB.
- Um post publicado deve possuir conteudo HTML valido no MongoDB.

### Tag

Regras:

- `name` obrigatorio.
- `slug` unico.
- Tags inativas nao devem ser associadas a novos posts.

### Usuario e Permissao

Regras:

- Usuario autenticado recebe permissoes via papeis.
- Uma permissao e composta por modulo e acao.
- As permissoes padrao devem ser semeadas via migration ou comando administrativo.

## 9. Permissoes

Enums sugeridos:

```python
from enum import Enum


class Acao(str, Enum):
    CRIAR = "criar"
    LER = "ler"
    ATUALIZAR = "atualizar"
    EXCLUIR = "excluir"


class Modulo(str, Enum):
    AUTH = "auth"
    POSTS = "posts"
    TAGS = "tags"
```

Permissoes padrao:

```python
PERMISSOES_PADRAO: dict[str, dict[str, list[Acao]]] = {
    "Master": {
        Modulo.AUTH.value: list(Acao),
        Modulo.POSTS.value: list(Acao),
        Modulo.TAGS.value: list(Acao),
    },
    "Editor": {
        Modulo.AUTH.value: [],
        Modulo.POSTS.value: [Acao.CRIAR, Acao.LER, Acao.ATUALIZAR],
        Modulo.TAGS.value: [
            Acao.CRIAR,
            Acao.LER,
            Acao.ATUALIZAR,
        ],
    },
    "Externo": {
        Modulo.POSTS.value: [Acao.LER,],
        Modulo.TAGS.value: [
            Acao.LER,
        ],

    }

}
```

Dependencia HTTP sugerida:

```python
def require_permission(module: Modulo, action: Acao):
    async def dependency(current_user: CurrentUser = Depends(get_current_user)):
        if not current_user.has_permission(module.value, action.value):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Permissao insuficiente",
            )
        return current_user

    return dependency
```

## 10. Casos de Uso

### Criar Post

Entrada:

- `title`.
- `slug`.
- `html`.
- `summary`.
- `tags`: array de slugs ou ids.

Fluxo:

1. Validar permissao `AUTH.:CRIAR` ou modulo equivalente de CMS.
2. Validar titulo, slug e HTML.
3. Validar tags existentes e ativas.
4. Criar documento no MongoDB com HTML.
5. Criar referencia no PostgreSQL com `mongo_object_id`, titulo, slug, status e autor.
6. Criar associacoes em `post_tags`.
7. Atualizar o documento MongoDB com `post_ref_id`, se necessario.
8. Retornar DTO do post.

Consistencia:

- Como nao ha transacao distribuida nativa entre PostgreSQL e MongoDB, o caso de uso deve compensar falhas.
- Se PostgreSQL falhar apos criar MongoDB, remover o documento MongoDB ou marcar como orfao para job de limpeza.
- Se MongoDB falhar, nenhuma referencia PostgreSQL deve ser persistida.

### Atualizar Post

Fluxo:

1. Validar permissao `AUTH.:ATUALIZAR`.
2. Buscar referencia no PostgreSQL.
3. Atualizar titulo, slug, status e tags no PostgreSQL.
4. Atualizar HTML e metadados no MongoDB.
5. Registrar auditoria.

### Publicar Post

Fluxo:

1. Validar permissao adequada.
2. Confirmar que o post possui `mongo_object_id`.
3. Confirmar que o documento MongoDB possui HTML nao vazio.
4. Alterar status para `published`.
5. Definir `published_at`.

### Upload de Imagem do Post

Fluxo:

1. Validar autenticacao e permissao de atualizacao do post.
2. Buscar post no PostgreSQL.
3. Obter `mongo_object_id`.
4. Validar tamanho maximo.
5. Validar MIME real com `python-magic`.
6. Rejeitar conteudo perigoso em preview textual.
7. Gerar nome seguro.
8. Salvar no MinIO com object key `upload/post/{ObjectId}/{safe_name}`.
9. Registrar imagem no documento MongoDB.
10. Retornar URL assinada ou endpoint controlado de download.

## 11. Portas da Aplicacao

Exemplos:

```python
from typing import Protocol


class PostReferenceRepository(Protocol):
    async def create(self, post: Post) -> Post: ...
    async def get_by_id(self, post_id: str) -> Post | None: ...
    async def get_by_slug(self, slug: str) -> Post | None: ...
    async def update(self, post: Post) -> Post: ...


class PostContentRepository(Protocol):
    async def create(self, content: PostContent) -> str: ...
    async def update(self, object_id: str, content: PostContent) -> None: ...
    async def get(self, object_id: str) -> PostContent | None: ...
    async def delete(self, object_id: str) -> None: ...


class ObjectStorage(Protocol):
    async def put_object(
        self,
        key: str,
        data: bytes,
        content_type: str,
        size: int,
    ) -> None: ...
```

## 12. API HTTP

Prefixo: `/api/v1`

### Auth

- `POST /auth/token`
- `POST /auth/refresh`
- `POST /auth/logout`
- `POST /auth/mfa/setup`
- `POST /auth/mfa/verify`

### Users

- `GET /users/me`
- `GET /users`
- `POST /users`
- `PATCH /users/{user_id}`
- `DELETE /users/{user_id}`

### Tags

- `GET /tags`
- `POST /tags`
- `GET /tags/{tag_id}`
- `PATCH /tags/{tag_id}`
- `DELETE /tags/{tag_id}`

### Posts

- `GET /posts`
- `POST /posts`
- `GET /posts/{post_id}`
- `GET /posts/slug/{slug}`
- `PATCH /posts/{post_id}`
- `POST /posts/{post_id}/publish`
- `POST /posts/{post_id}/archive`
- `DELETE /posts/{post_id}`

### Uploads

- `POST /posts/{post_id}/images`
- `GET /posts/{post_id}/images/{image_id}/download`
- `DELETE /posts/{post_id}/images/{image_id}`

## 13. Schemas HTTP

### Criar Post

```json
{
  "title": "Titulo da materia",
  "slug": "titulo-da-materia",
  "html": "<p>Conteudo</p>",
  "summary": "Resumo da materia",
  "tags": ["educacao", "noticias"]
}
```

### Resposta de Post

```json
{
  "id": "6f5fb9f4-30e5-48f4-8aa7-fb841e2a9915",
  "mongo_object_id": "665f0d9f8f1b2f9a9f8c0001",
  "title": "Titulo da materia",
  "slug": "titulo-da-materia",
  "status": "draft",
  "tags": [
    {
      "id": 1,
      "name": "Educacao",
      "slug": "educacao"
    }
  ],
  "created_at": "2026-05-20T00:00:00Z",
  "updated_at": "2026-05-20T00:00:00Z"
}
```

## 14. Upload Seguro

Regras:

- Nunca confiar no nome do arquivo enviado pelo usuario.
- Nunca montar caminho diretamente com input do usuario.
- Usar `python-magic` para detectar MIME real.
- Validar tamanho maximo no endpoint e no stream.
- Gerar nome criptograficamente seguro.
- Salvar no MinIO, nao em static mount publico.
- Download deve ser controlado pela API ou por URL assinada de curta duracao.
- Para conteudo sensivel, usar `Content-Disposition: attachment`.

Tipos permitidos inicialmente:

- `image/jpeg`
- `image/png`
- `image/webp`

PDF pode ser suportado em modulo de documentos, mas nao deve ser aceito como imagem de post.

Exemplo de funcao de nome seguro:

```python
import secrets


ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def generate_safe_filename(content_type: str) -> str:
    random_suffix = secrets.token_urlsafe(16)
    ext = ALLOWED_IMAGE_TYPES.get(content_type, ".bin")
    return f"{random_suffix}{ext}"
```

Object key:

```text
upload/post/{mongo_object_id}/{safe_filename}
```

## 15. Middleware e Observabilidade

O middleware de tempo de requisicao deve ser adaptado para ASGI/FastAPI.

Responsabilidades:

- Criar `request_id`.
- Salvar `request_id` em `ContextVar`.
- Medir duracao.
- Logar metodo, path, status e tempo.
- Marcar requisicoes acima de 1000 ms como lentas.

Exemplo:

```python
import time
import uuid
from contextvars import ContextVar
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


request_id_var: ContextVar[str] = ContextVar("request_id", default="")


class TempoRequisicaoMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())[:8]
        request_id_var.set(request_id)
        inicio = time.perf_counter()

        response = await call_next(request)

        duracao_ms = (time.perf_counter() - inicio) * 1000
        payload = {
            "request_id": request_id,
            "method": request.method,
            "path": str(request.url.path),
            "status_code": response.status_code,
            "duration_ms": round(duracao_ms, 2),
        }

        if duracao_ms > 1000:
            logger.warning("Requisicao lenta", **payload)
        else:
            logger.info("Requisicao finalizada", **payload)

        response.headers["X-Request-ID"] = request_id
        return response
```

## 16. Rate Limit

Usar `slowapi` com Redis.

Rotas sensiveis:

- `POST /auth/token`: limite agressivo por IP e usuario.
- `POST /auth/mfa/verify`.
- Uploads de arquivos.
- Criacao de posts.

Exemplo de politicas:

- Login: `5/minute`.
- Upload: `30/minute`.
- Leitura publica de posts publicados: `120/minute`.

## 17. Erros e Excecoes

Excecoes de dominio devem ser independentes de HTTP:

```python
class AuthException(Exception):
    def __init__(self, username: str, user=None):
        super().__init__(username, user)
        self.username = username
        self.user = user


class UsernameAlreadyExists(AuthException):
    pass


class PasswordTooShort(AuthException):
    pass
```

A camada `presentation/http/error_handlers.py` converte excecoes para `HTTPException` ou respostas JSON com `HTTPStatus`.

Padrao de resposta:

```json
{
  "detail": "Permissao insuficiente",
  "code": "permission_denied",
  "request_id": "a1b2c3d4"
}
```

## 18. Autenticacao

Requisitos:

- Login por email e senha.
- Hash de senha com Argon2 via `pwdlib[argon2]`.
- Token JWT com `sub`, `email`, `roles` e expiracao.
- Refresh token, se necessario, armazenado com estrategia revogavel.
- MFA/TOTP opcional usando `pyotp`.
- QR Code de setup usando `qrcode[pil]`.

Cuidados:

- Nunca logar senha, token completo ou segredo TOTP.
- Rate limit em login e MFA.
- Invalidar sessoes quando senha for alterada.

## 19. Jobs Assincronos com ARQ

Usar ARQ com Redis para tarefas fora da requisicao:

- Remover conteudos orfaos no MongoDB.
- Remover objetos orfaos no MinIO.
- Gerar resumo ou texto limpo do HTML.
- Processar imagens, se houver otimizacao futura.
- Emitir eventos de auditoria pesados.

## 20. Auditoria

Eventos recomendados:

- Login com sucesso.
- Falha de login.
- Criacao, atualizacao, publicacao e exclusao de post.
- Upload e exclusao de imagem.
- Alteracao de permissao.
- Alteracao de usuario ou papel.

Tabela `audit_logs` no PostgreSQL:

- `id`.
- `actor_user_id`.
- `action`.
- `resource_type`.
- `resource_id`.
- `metadata` JSONB.
- `ip_address`.
- `user_agent`.
- `created_at`.

## 21. Testes

### Organizacao

```text
tests/
  conftest.py
  factories/
    users.py
    posts.py
    tags.py
  unit/
    domain/
    application/
  integration/
    http/
    postgres/
    mongodb/
    minio/
```

### Fixtures PostgreSQL

Basear `tests/conftest.py` no padrao abaixo:

```python
from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from app.infrastructure.postgres.database import get_session
from app.infrastructure.postgres.models import table_registry
from app.main import app
from app.core.security import get_password_hash
from tests.factories.users import UserFactory


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def engine():
    with PostgresContainer("postgres:18", driver="psycopg") as postgres:
        engine = create_async_engine(
            postgres.get_connection_url().replace(
                "postgresql+psycopg://",
                "postgresql+psycopg_async://",
                1,
            )
        )
        try:
            yield engine
        finally:
            await engine.dispose()


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def db_schema(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture
async def reset_db(engine, db_schema):
    table_names = ", ".join(
        table.name for table in reversed(table_registry.metadata.sorted_tables)
    )
    if table_names:
        async with engine.begin() as conn:
            await conn.execute(
                text(f"TRUNCATE {table_names} RESTART IDENTITY CASCADE")
            )

    yield


@pytest_asyncio.fixture
async def session(engine, reset_db):
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
        await session.rollback()


@pytest.fixture
def client(engine, reset_db):
    async def get_session_override():
        async with AsyncSession(engine, expire_on_commit=False) as session:
            yield session

    client = TestClient(app)
    app.dependency_overrides[get_session] = get_session_override
    yield client

    app.dependency_overrides.clear()
    client.close()


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time
        if hasattr(target, "updated_at"):
            target.updated_at = time

    event.listen(model, "before_insert", fake_time_hook)

    yield time

    event.remove(model, "before_insert", fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session):
    password = "testtest"
    user = UserFactory(password=get_password_hash(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def other_user(session):
    password = "testtest"
    user = UserFactory(password=get_password_hash(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def token(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": user.clean_password},
    )
    return response.json()["access_token"]
```

### Testes Obrigatorios

- Criar tag.
- Impedir tag duplicada por slug.
- Criar post com array de tags.
- Persistir HTML no MongoDB.
- Persistir `mongo_object_id`, titulo e tags no PostgreSQL.
- Publicar post apenas com conteudo MongoDB valido.
- Upload rejeita MIME nao permitido.
- Upload salva objeto no caminho `upload/post/{ObjectId}`.
- Usuario sem permissao recebe HTTP 403.
- Login retorna JWT valido.
- Rate limit bloqueia abuso em login.

## 22. Integracao com Vue.js 3.5

O frontend deve consumir a API via JSON e enviar arquivos via `multipart/form-data`.

Validacoes recomendadas no frontend:

- Validar tamanho antes do upload.
- Usar `file-type` para detectar assinatura real do arquivo.
- Exibir erro de MIME invalido antes de enviar.
- Enviar tags como array de slugs ou ids.
- Manter editor HTML separado do fluxo de upload de imagem.

Contrato de upload:

```http
POST /api/v1/posts/{post_id}/images
Content-Type: multipart/form-data
Authorization: Bearer <token>
```

Resposta:

```json
{
  "image_id": "generated-id",
  "object_key": "upload/post/665f0d9f8f1b2f9a9f8c0001/abc123.jpg",
  "url": "/api/v1/posts/{post_id}/images/{image_id}/download"
}
```

## 23. Migracoes e Seeds

Alembic deve criar:

- Usuarios.
- Papeis.
- Permissoes.
- Tags.
- Posts.
- Post tags.
- Auditoria.

Seeds iniciais:

- Papel `Master`.
- Papel `Editor`.
- Permissoes padrao.
- Usuario admin inicial somente em ambiente local ou por comando seguro.

## 24. Decisoes Arquiteturais

### PostgreSQL como fonte de listagem

Listagens de posts devem consultar PostgreSQL para evitar carregar HTML do MongoDB sem necessidade.

### MongoDB para conteudo HTML

O HTML pode crescer, mudar de estrutura e incluir dados editoriais flexiveis. MongoDB reduz atrito para evolucao desse documento.

### MinIO para imagens

Imagens nao devem ficar no banco. MinIO permite armazenamento S3-compatible, organizacao por post e futura troca por S3 real.

### Sem transacao distribuida

PostgreSQL e MongoDB nao devem depender de transacao distribuida. O sistema deve usar compensacao e jobs de limpeza para recursos orfaos.

## 25. Criterios de Aceite

- Projeto FastAPI inicia com `uvicorn`.
- Configuracoes carregam por `.env`.
- PostgreSQL usa SQLAlchemy AsyncIO e Alembic.
- MongoDB usa Motor.
- Tags possuem CRUD.
- Posts aceitam array de tags.
- PostgreSQL armazena `mongo_object_id`, titulo, slug, status e tags.
- MongoDB armazena HTML da materia.
- Upload de imagem salva no MinIO em `upload/post/{ObjectId}`.
- Permissoes por modulo e acao protegem endpoints.
- Testes rodam com Pytest e Testcontainers.
- Lint passa com Ruff.
- Cobertura minima inicial recomendada: 80%.

## 26. Roadmap de Implementacao

1. Criar projeto Poetry e estrutura de pastas.
2. Configurar FastAPI, settings, logs e middleware.
3. Configurar PostgreSQL AsyncIO e Alembic.
4. Criar modelos de usuarios, papeis, permissoes, tags e posts.
5. Configurar MongoDB com Motor.
6. Implementar portas e repositorios.
7. Implementar casos de uso de tags.
8. Implementar casos de uso de posts.
9. Implementar autenticacao e autorizacao.
10. Configurar MinIO e upload seguro.
11. Adicionar Redis, slowapi e ARQ.
12. Criar fixtures e testes de integracao.
13. Documentar OpenAPI e contratos para Vue.js.

