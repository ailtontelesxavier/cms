# [1] Bootstrap do Projeto Frontend

# [1] Bootstrap do Projeto Frontend Vue 3

## Objetivo

Inicializar o projeto Vue 3 + TypeScript + Vite em `frontend/`, configurar Tailwind CSS v4, scripts, variáveis de ambiente e confirmar que a aplicação sobe localmente.

## Tarefas

### 1.1 Inicializar projeto com Vite

Executar `npm create vite@latest frontend -- --template vue-ts` na raiz do repositório. Confirmar que `frontend/package.json` contém os scripts `dev`, `build` e `preview`.

### 1.2 Instalar dependências principais

**Dependências de produção:**

| Pacote | Versão | Finalidade |
| --- | --- | --- |
| `vue-router` | ^4 | Roteamento SPA |
| `pinia` | ^2 | Estado global |
| `axios` | ^1 | Cliente HTTP |
| `@editorjs/editorjs` | 2.31.x | Editor de conteúdo |
| `@editorjs/header` | latest | Bloco de cabeçalho |
| `@editorjs/list` | latest | Bloco de lista |
| `@editorjs/image` | latest | Bloco de imagem |
| `@editorjs/quote` | latest | Bloco de citação |
| `@editorjs/code` | latest | Bloco de código |
| `@editorjs/delimiter` | latest | Bloco delimitador |
| `file-type` | latest | Validação de MIME no cliente |

**Dependências de desenvolvimento:**

| Pacote | Versão | Finalidade |
| --- | --- | --- |
| `tailwindcss` | ^4 | Framework CSS utilitário |
| `@tailwindcss/vite` | ^4 | Plugin Vite para Tailwind v4 |

### 1.2.1 Configurar Tailwind CSS v4

O Tailwind v4 **não usa** `tailwind.config.js` nem `postcss.config.js`. A integração é feita exclusivamente via plugin Vite:

1. Adicionar `tailwindcss()` ao array `plugins` em file:frontend/vite.config.ts (junto com o plugin `vue()`).
2. Criar file:frontend/src/style.css com uma única linha: `@import 'tailwindcss';`.
3. Importar `./style.css` em file:frontend/src/main.ts.

Não criar `tailwind.config.js` — no v4 a configuração é feita via diretivas CSS (`@theme`, `@layer`) quando necessário.

### 1.3 Configurar variáveis de ambiente

Criar `frontend/.env.example`:

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Criar `frontend/.env.local` (não versionado) com o valor local.

### 1.4 Estrutura de pastas inicial

Criar a estrutura de diretórios conforme o SDD: `src/api/`, `src/stores/`, `src/router/`, `src/types/`, `src/modules/`, `src/shared/`.

### 1.5 Verificação

- `npm run dev` sobe sem erros.
- `npm run build` compila sem erros de TypeScript.
- `VITE_API_BASE_URL` é acessível via `import.meta.env.VITE_API_BASE_URL`.
- Classes Tailwind como `bg-slate-800` e `text-white` funcionam em componentes `.vue`.

## Arquivos Criados

| Arquivo | Descrição |
| --- | --- |
| file:frontend/package.json | Dependências e scripts |
| file:frontend/vite.config.ts | Configuração Vite |
| file:frontend/tsconfig.json | Configuração TypeScript |
| file:frontend/.env.example | Template de variáveis de ambiente |
| file:frontend/src/main.ts | Entrypoint da aplicação |
| file:frontend/src/App.vue | Root component |
| file:frontend/src/style.css | CSS global com `@import 'tailwindcss'` |