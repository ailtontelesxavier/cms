# [Frontend] App Shell — Layout Autenticado com Tailwind v4

## Objetivo

Implementar o layout autenticado da aplicação: sidebar de navegação, header com usuário logado e estrutura de `RouterView`. Toda a estilização usa exclusivamente classes Tailwind v4.

Referência: spec:94772f59-b09f-4841-b5c0-dc363baa319c/fb1b6a8a-b9e8-48f9-bd7e-fef77df21870.

## Componentes

### `AppLayout.vue` (file:frontend/src/modules/app-shell/components/AppLayout.vue)

Layout raiz para rotas autenticadas. Estrutura de grid com sidebar fixa à esquerda e área de conteúdo principal à direita. Usa `<RouterView>` para renderizar a view ativa. Não contém lógica de negócio.

Estrutura visual:

```wireframe

<html>
<head>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; font-family: sans-serif; }
body { display: flex; height: 100vh; background: #f8fafc; }
.sidebar { width: 224px; background: #0f172a; color: #fff; display: flex; flex-direction: column; flex-shrink: 0; }
.logo { padding: 20px; font-size: 17px; font-weight: 700; border-bottom: 1px solid #1e293b; letter-spacing: -0.01em; }
.nav { flex: 1; padding: 12px 8px; display: flex; flex-direction: column; gap: 2px; }
.nav-link { display: flex; align-items: center; gap: 10px; padding: 9px 12px; border-radius: 6px; font-size: 14px; color: #94a3b8; text-decoration: none; }
.nav-link.active { background: #1e293b; color: #f1f5f9; }
.nav-link:hover { background: #1e293b; color: #cbd5e1; }
.sidebar-footer { padding: 16px; border-top: 1px solid #1e293b; }
.user-info { font-size: 13px; color: #64748b; margin-bottom: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.logout-btn { width: 100%; padding: 7px; background: transparent; border: 1px solid #334155; border-radius: 5px; color: #64748b; font-size: 13px; cursor: pointer; }
.main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.header { background: #fff; border-bottom: 1px solid #e2e8f0; padding: 0 24px; height: 56px; display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; }
.page-title { font-size: 16px; font-weight: 600; color: #0f172a; }
.user-badge { display: flex; align-items: center; gap: 8px; }
.avatar { width: 32px; height: 32px; border-radius: 50%; background: #3b82f6; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 600; }
.user-name { font-size: 14px; color: #475569; }
.content { flex: 1; overflow-y: auto; padding: 24px; }
</style>
</head>
<body>
<div class="sidebar">
  <div class="logo">CMS Admin</div>
  <nav class="nav">
    <a class="nav-link active" href="#">📄 Posts</a>
    <a class="nav-link" href="#">🏷️ Tags</a>
  </nav>
  <div class="sidebar-footer">
    <div class="user-info">admin@cms.local</div>
    <button class="logout-btn">Sair</button>
  </div>
</div>
<div class="main">
  <header class="header">
    <span class="page-title">Posts</span>
    <div class="user-badge">
      <div class="avatar">A</div>
      <span class="user-name">Admin</span>
    </div>
  </header>
  <div class="content">

  </div>
</div>
</body>
</html>
```

### `AppSidebar.vue`

- Links de navegação para `/posts` e `/tags` com destaque de rota ativa via `RouterLinkActive`.
- Email do usuário autenticado lido da session store.
- Botão "Sair" chama `sessionStore.logout()`.
- Estilização: fundo `bg-slate-900`, links com `hover:bg-slate-800`, link ativo com `bg-slate-800 text-slate-100`.

### `AppHeader.vue`

- Título da página via `useRoute().meta.title`.
- Avatar com inicial do nome do usuário (fundo `bg-blue-500`).
- Nome do usuário autenticado.

## Critérios de Aceite

Layout renderiza sidebar + header + RouterView sem sobreposições.Link ativo na sidebar é destacado visualmente.Botão "Sair" encerra a sessão e redireciona para /login.Título no header muda conforme a rota ativa.Layout é responsivo: sidebar não colapsa (admin desktop-first).Nenhum estilo inline ou CSS externo — apenas classes Tailwind v4.