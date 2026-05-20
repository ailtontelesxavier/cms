## Why

O repositório já possui um backend CMS em FastAPI pronto para ser consumido por um painel administrativo, mas o frontend ainda não existe. Criar esse projeto agora destrava o uso operacional do CMS, valida os fluxos HTTP já implementados e estabelece a base do produto para evolução futura.

## What Changes

- Criar um projeto frontend dedicado em Vue.js 3 para o painel administrativo do CMS.
- utilizar editorjs version 2.31
- Implementar a base de aplicação para ambiente web administrativo, incluindo roteamento, layout autenticado, configuração por ambiente e cliente HTTP para a API `/api/v1`.
- Implementar autenticação administrativa com login, refresh de sessão, logout e fluxo de MFA quando exigido pelo backend.
- Implementar a interface inicial de gestão editorial para tags e posts, incluindo listagem, criação, edição, publicação, arquivamento e upload de imagens de posts.
- Alinhar contratos mínimos do backend que hoje impedem alguns fluxos do admin, especialmente MFA de login, leitura detalhada do conteúdo de posts e identificação consistente de imagens.
- Padronizar o tratamento de estados de carregamento, erros de API e proteção de rotas autenticadas para permitir evolução segura do frontend.

## Capabilities

### New Capabilities
- `admin-app-shell`: Estrutura base do projeto Vue 3 com boot da aplicação, roteamento, layout autenticado, configuração por ambiente e integração HTTP com o backend.
- `admin-auth-session`: Fluxo de autenticação administrativa com login, MFA, refresh de token, logout e proteção de rotas privadas.
- `admin-content-management`: Interface administrativa para operar tags, posts e imagens com os endpoints já existentes do CMS.

### Modified Capabilities
- None.

## Impact

- Afeta a pasta `frontend/`, que passará a conter o projeto Vue.js 3 do admin.
- Consome os endpoints já expostos pelo backend FastAPI para auth, tags, posts e uploads, com ajustes pontuais de contrato onde o backend atual ainda não cobre o fluxo administrativo completo.
- Introduz dependências de frontend para Vue 3, roteamento, gerenciamento de estado/sessão, cliente HTTP e ferramenta de build.
- Define a primeira experiência administrativa do CMS e servirá de base para capacidades futuras, como gestão de usuários e dashboards.