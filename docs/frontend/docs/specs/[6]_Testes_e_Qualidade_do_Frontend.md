# [6] Testes e Qualidade do Frontend

# [6] Testes e Qualidade do Frontend

## Objetivo

Definir a estratégia de testes automatizados, lint e critérios de qualidade para o frontend Vue 3.

## Stack de Testes

| Ferramenta | Finalidade |
| --- | --- |
| Vitest | Test runner (integrado ao Vite) |
| Vue Test Utils | Montagem e interação com componentes |
| `@testing-library/vue` | Queries semânticas nos testes de componente |
| `msw` (Mock Service Worker) | Mock de requisições HTTP nos testes |

## Cobertura Mínima

| Módulo | Cobertura alvo |
| --- | --- |
| `stores/session.ts` | 90% |
| `api/client.ts` | 80% |
| `composables/useTags.ts` | 80% |
| `composables/usePosts.ts` | 80% |
| Componentes críticos | 70% |

## Testes Obrigatórios

### Session Store

| # | Cenário |
| --- | --- |
| 1 | Login com credenciais válidas persiste token e popula `currentUser` |
| 2 | Login com credenciais inválidas mantém `isAuthenticated = false` |
| 3 | `restoreSession` com token válido no `sessionStorage` hidrata usuário |
| 4 | `restoreSession` sem token mantém estado não autenticado |
| 5 | `logout` limpa `sessionStorage` e estado |
| 6 | Interceptor 401 chama `logout` e redireciona para `/login` |

### Router Guard

| # | Cenário |
| --- | --- |
| 7 | Rota protegida sem sessão redireciona para `/login?redirect=...` |
| 8 | Rota protegida com sessão válida permite acesso |
| 9 | Rota pública é acessível sem sessão |

### Tags

| # | Cenário |
| --- | --- |
| 10 | `useTags.fetchTags` popula lista e total |
| 11 | `useTags.createTag` chama API e atualiza lista |
| 12 | Erro 409 em `createTag` expõe `fieldErrors.slug` |
| 13 | `useTags.deleteTag` remove item da lista após sucesso |

### Posts

| # | Cenário |
| --- | --- |
| 14 | `usePosts.fetchPosts` com filtro de status passa query param correto |
| 15 | `usePosts.publishPost` chama endpoint correto e atualiza status |
| 16 | `usePosts.archivePost` chama endpoint correto e atualiza status |

### Upload de Imagem

| # | Cenário |
| --- | --- |
| 17 | `usePostImages.uploadImage` envia `multipart/form-data` e retorna `UploadImageOut` |
| 18 | Arquivo com MIME inválido é rejeitado antes de enviar ao backend |

## Lint e Formatação

| Ferramenta | Configuração |
| --- | --- |
| ESLint | `@vue/eslint-config-typescript` + `eslint-plugin-vue` |
| Prettier | Integrado ao ESLint via `eslint-config-prettier` |

Scripts no `package.json`:

```
"lint": "eslint src --ext .ts,.vue"
"format": "prettier --write src"
"test": "vitest"
"test:coverage": "vitest --coverage"
```

## Documentação Local

O arquivo `frontend/README.md` deve cobrir:

1. Pré-requisitos (Node.js, npm).
2. Instalação de dependências.
3. Configuração do `.env.local`.
4. Como iniciar o backend local.
5. Como rodar o frontend em desenvolvimento.
6. Como rodar os testes.
7. Gaps de contrato conhecidos com o backend.