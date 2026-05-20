# CMS Admin — Frontend

Painel administrativo do CMS, construído com Vue 3 + TypeScript + Vite.

## Stack

- **Framework**: Vue 3 (Composition API, `<script setup>`, TypeScript)
- **Build**: Vite
- **Roteamento**: vue-router 4
- **Estado**: Pinia
- **HTTP**: Axios
- **Estilização**: Tailwind CSS v4

## Pré-requisitos

- Node.js >= 18
- Backend CMS rodando em `http://localhost:8000`

## Setup

```bash
cd frontend
npm install
```

## Variáveis de Ambiente

| Variável | Descrição | Padrão |
|---|---|---|
| `VITE_API_BASE_URL` | URL base da API do backend | `http://localhost:8000/api/v1` |

Arquivos de ambiente:

- `.env` — valores padrão compartilhados
- `.env.development` — overrides para desenvolvimento (usado por `npm run dev`)
- `.env.production` — overrides para produção (usado por `npm run build`)

## Scripts

```bash
npm run dev       # Inicia servidor de desenvolvimento
npm run build     # Compila para produção
npm run preview   # Preview da build de produção
npm run test      # Executa testes uma vez
npm run test:watch  # Executa testes em modo watch
```

## Estrutura do Projeto

```
src/
  app-shell/               # Layout global, roteamento, guards de autenticação
    router/                # Configuração do vue-router
    components/            # AppLayout, sidebar
  auth-session/            # Autenticação e sessão
    stores/                # Pinia store de sessão
    views/                 # Login, MFA Challenge, MFA Setup, MFA Verify
    components/
  content-management/      # Gestão de conteúdo
    tags/                  # CRUD de tags
    posts/                 # CRUD de posts
    images/                # Upload de imagens
  shared/                  # Camada compartilhada
    api/                   # Cliente HTTP (Axios) e serviços por recurso
    types/                 # Interfaces TypeScript
    ui/                    # Componentes base (LoadingSpinner, EmptyState, ApiError)
    composables/
```

## Rotas

| Caminho | Nome | Autenticação |
|---|---|---|
| `/login` | login | Pública |
| `/mfa-required` | mfa-required | Pública |
| `/` | — | Protegida (redireciona para /posts) |
| `/mfa/setup` | mfa-setup | Protegida |
| `/mfa/verify` | mfa-verify | Protegida |
| `/tags` | tags | Protegida |
| `/tags/new` | tag-create | Protegida |
| `/tags/:id/edit` | tag-edit | Protegida |
| `/posts` | posts | Protegida |
| `/posts/new` | post-create | Protegida |
| `/posts/:id/edit` | post-edit | Protegida |

## Contratos do Backend

### Autenticação

- `POST /api/v1/auth/token` — Login com email+senha. Retorna `{ access_token, refresh_token, token_type }`. Se MFA estiver habilitado, retorna `403` com detalhe `auth:mfa_required`.
- `POST /api/v1/auth/refresh` — Renova tokens usando `refresh_token`.
- `POST /api/v1/auth/mfa/challenge` — Login com email+senha+TOTP para contas com MFA habilitado.
- `POST /api/v1/auth/mfa/setup` — Gera secret TOTP e QR Code.
- `POST /api/v1/auth/mfa/verify` — Ativa MFA após validar código TOTP.
- `GET /api/v1/users/me` — Retorna dados do usuário autenticado.

### Posts

- `GET /api/v1/posts` — Lista paginada com filtro opcional por `status`.
- `GET /api/v1/posts/{id}` — Metadados do post (sem conteúdo HTML).
- `GET /api/v1/posts/{id}/detail` — Post com conteúdo HTML, summary e metadados das imagens.
- `POST /api/v1/posts` — Criar post (requer `posts:criar`).
- `PATCH /api/v1/posts/{id}` — Atualizar post (requer `posts:atualizar`).
- `POST /api/v1/posts/{id}/publish` — Publicar post.
- `POST /api/v1/posts/{id}/archive` — Arquivar post.
- `DELETE /api/v1/posts/{id}` — Excluir post (requer `posts:excluir`).

### Tags

- `GET /api/v1/tags` — Lista paginada de tags.
- `POST /api/v1/tags` — Criar tag (requer `tags:criar`).
- `GET /api/v1/tags/{id}` — Detalhe da tag.
- `PATCH /api/v1/tags/{id}` — Atualizar tag (requer `tags:atualizar`).
- `DELETE /api/v1/tags/{id}` — Excluir tag (requer `tags:excluir`).

### Imagens

- `POST /api/v1/posts/{post_id}/images` — Upload de imagem (JPEG, PNG, WebP).
- `GET /api/v1/posts/{post_id}/images/{img_id}/download` — URL para download.
- `DELETE /api/v1/posts/{post_id}/images/{img_id}` — Remover imagem.

### Paginação

Todas as listagens retornam `{ items: [], total: number, page: number, page_size: number, pages: number }`.
