# [Frontend] Bootstrap, Tailwind v4 e Infraestrutura Base

## Objetivo

Inicializar o projeto Vue 3 + TypeScript + Vite em `frontend/`, instalar e configurar Tailwind CSS v4, criar a camada HTTP compartilhada, o router com guards e os componentes base reutilizáveis.

Referências: spec:94772f59-b09f-4841-b5c0-dc363baa319c/46fed2e7-afb8-47ee-8f64-a0e87850bff1, spec:94772f59-b09f-4841-b5c0-dc363baa319c/fb1b6a8a-b9e8-48f9-bd7e-fef77df21870.

## Escopo

### 1. Inicialização do projeto

- Criar projeto com `npm create vite@latest frontend -- --template vue-ts`.
- Instalar dependências de produção: `vue-router@^4`, `pinia@^2`, `axios@^1`.
- Instalar dependências de desenvolvimento: `tailwindcss@^4`, `@tailwindcss/vite@^4`.
- Configurar file:frontend/vite.config.ts com os plugins `vue()` e `tailwindcss()`.
- Criar file:frontend/src/style.css com `@import 'tailwindcss'` e importar em `main.ts`.
- Criar file:frontend/.env.example com `VITE_API_BASE_URL=http://localhost:8000/api/v1`.
- Criar estrutura de pastas: `src/api/`, `src/stores/`, `src/router/`, `src/types/`, `src/modules/`, `src/shared/`.

### 2. Cliente HTTP (file:frontend/src/api/client.ts)

- Instância axios com `baseURL` lida de `import.meta.env.VITE_API_BASE_URL`.
- Request interceptor: injeta `Authorization: Bearer <token>` da session store quando disponível.
- Response interceptor: trata `401` (limpa sessão + redireciona para `/login`) e normaliza erros `403`, `409`, `422` e de rede para o formato `{ status, detail, code, fieldErrors }`.

### 3. Router (file:frontend/src/router/index.ts)

Rotas conforme o SDD:

| Path | Componente | Guard |
| --- | --- | --- |
| `/login` | `LoginView` | público |
| `/mfa/verify` | `MfaTotpView` | público |
| `/` | redirect `/posts` | — |
| `/posts` | `PostsView` | autenticado |
| `/posts/new` | `PostEditView` | autenticado |
| `/posts/:id/edit` | `PostEditView` | autenticado |
| `/tags` | `TagsView` | autenticado |

Navigation guard `beforeEach`: verifica `meta.requiresAuth` e `sessionStore.isAuthenticated`. Redireciona para `/login?redirect=<destino>` quando não autenticado.

### 4. Componentes base (file:frontend/src/shared/components/)

Todos estilizados com classes Tailwind v4:

| Componente | Descrição |
| --- | --- |
| `BaseButton.vue` | Props: `variant` (`primary`/`secondary`/`danger`), `loading`, `disabled`. Spinner inline quando `loading=true`. |
| `BaseModal.vue` | Overlay com slot de conteúdo e prop `title`. Fecha com Esc e clique no overlay. |
| `BasePagination.vue` | Props: `page`, `total`, `pageSize`. Emite `update:page`. |
| `LoadingSpinner.vue` | SVG animado, prop `size` (`sm`/`md`/`lg`). |
| `EmptyState.vue` | Props: `message`, `icon?`. Centralizado com ícone opcional. |
| `ApiErrorAlert.vue` | Props: `error: ApiError |

### 5. Composable `useApiError` (file:frontend/src/shared/composables/useApiError.ts)

- Recebe erro bruto do axios.
- Extrai `detail`, `code` e `fieldErrors` (erros de campo do Pydantic 422).
- Expõe `errorMessage: string` e `fieldErrors: Record<string, string>`.

## Critérios de Aceite

npm run dev sobe sem erros em frontend/.npm run build compila sem erros de TypeScript.Classes Tailwind (bg-slate-800, text-white, rounded-lg) funcionam em componentes .vue.Não existe tailwind.config.js nem postcss.config.js no projeto.Rota protegida sem sessão redireciona para /login?redirect=<destino>.Rota pública é acessível sem sessão.BaseButton exibe spinner quando loading=true e fica desabilitado.ApiErrorAlert exibe mensagem de erro normalizada.