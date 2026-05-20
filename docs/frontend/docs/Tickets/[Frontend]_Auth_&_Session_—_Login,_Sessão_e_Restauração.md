# [Frontend] Auth & Session — Login, Sessão e Restauração

## Objetivo

Implementar o fluxo completo de autenticação: tela de login, Pinia store de sessão com persistência em `sessionStorage`, restauração no reload e renovação via refresh token.

Referência: spec:94772f59-b09f-4841-b5c0-dc363baa319c/a765621d-61a0-41e7-96e1-4c6a0eb01efd.

## Session Store (file:frontend/src/stores/session.ts)

Estado persistido em `sessionStorage`:

| Campo | Tipo | Persistência |
| --- | --- | --- |
| `accessToken` | `string \| null` | `sessionStorage` |
| `refreshToken` | `string \| null` | `sessionStorage` |
| `currentUser` | `UserOut \| null` | memória |

Actions: `login(email, password)`, `loadCurrentUser()`, `refresh()`, `logout()`, `restoreSession()`.
Getters: `isAuthenticated`, `userDisplayName`.

A action `restoreSession()` deve ser chamada em `App.vue` no `onMounted`, antes do router processar a primeira navegação.

## Composable `useLogin` (file:frontend/src/modules/auth-session/composables/useLogin.ts)

- Expõe `email`, `password`, `isLoading`, `error`.
- `submit()`: chama `sessionStore.login()`. Se a resposta contiver `mfa_required: true`, armazena `pre_auth_token` em estado reativo transitório e navega para `/mfa/verify`. Caso contrário, redireciona para o destino salvo em `?redirect` ou para `/posts`.

## Tela de Login (file:frontend/src/modules/auth-session/views/LoginView.vue)

Estilizada com Tailwind v4. Card centralizado na tela com campos de email e senha, botão de submit com estado de loading e exibição de erro.

```wireframe

<html>
<head>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; font-family: sans-serif; }
body { background: #f1f5f9; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
.card { background: #fff; border-radius: 12px; padding: 40px; width: 380px; box-shadow: 0 4px 24px rgba(0,0,0,0.07); }
.logo { text-align: center; font-size: 22px; font-weight: 700; color: #0f172a; margin-bottom: 6px; }
.sub { text-align: center; font-size: 14px; color: #64748b; margin-bottom: 28px; }
.field { margin-bottom: 18px; }
label { display: block; font-size: 13px; font-weight: 500; color: #374151; margin-bottom: 5px; }
input { width: 100%; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px; }
input:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59,130,246,0.1); }
.btn { width: 100%; padding: 11px; background: #2563eb; color: #fff; border: none; border-radius: 6px; font-size: 15px; font-weight: 500; cursor: pointer; }
.error { background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px; padding: 10px 14px; font-size: 13px; color: #dc2626; margin-bottom: 16px; }
</style>
</head>
<body>
<div class="card">
  <div class="logo">CMS Admin</div>
  <div class="sub">Acesse o painel administrativo</div>
  <div class="error">Credenciais inválidas. Tente novamente.</div>
  <div class="field"><label>E-mail</label><input type="email" placeholder="admin@cms.local" /></div>
  <div class="field"><label>Senha</label><input type="password" placeholder="••••••••" /></div>
  <button class="btn">Entrar</button>
</div>
</body>
</html>
```

## Tipos (file:frontend/src/types/auth.ts)

```
interface TokenOut { access_token: string; refresh_token?: string; token_type: string }
interface MfaLoginRequired { mfa_required: true; pre_auth_token: string }
type LoginResponse = TokenOut | MfaLoginRequired
interface UserOut { id: string; email: string; name: string; is_active: boolean; is_superuser: boolean; mfa_enabled: boolean; roles: string[] }
```

## Critérios de Aceite

Login com credenciais válidas persiste access_token em sessionStorage e redireciona para /posts.Login com credenciais inválidas exibe mensagem de erro sem limpar os campos.Reload da página com sessão válida mantém o usuário autenticado (sem redirecionar para login).logout() limpa sessionStorage e redireciona para /login.Interceptor 401 do axios chama logout() automaticamente.Login com usuário MFA habilitado navega para /mfa/verify (integração com ticket ).