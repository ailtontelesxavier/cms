# [6] Autenticação, autorização e MFA

> **Status:** ✅ Implementado

## Objetivo

Implementar autenticação JWT com Argon2, refresh token, MFA/TOTP e o sistema de permissões por módulo/ação.

## Tarefas

- [x] Implementar `app/core/security.py`: hash Argon2, geração/validação JWT, geração de TOTP secret e QR Code.
- [x] Criar entidades de domínio em `domain/auth/`: `User`, `Permission`, `Role`, value objects, exceções.
- [x] Implementar casos de uso em `application/auth/use_cases.py`: login, refresh, logout, setup MFA, verify MFA.
- [x] Implementar dependência HTTP `require_permission(module, action)` em `presentation/http/dependencies.py`.
- [x] Implementar `get_current_user` com validação de JWT e carregamento de permissões.
- [x] Implementar router `presentation/http/routers/auth.py` e `users.py`.
- [x] Aplicar rate limit em `/auth/token` (5/min) e `/auth/mfa/verify`.

## Critérios de Aceite

- `POST /auth/token` retorna JWT válido com `sub`, `email`, `roles`.
- Token expirado retorna HTTP 401.
- Usuário sem permissão retorna HTTP 403.
- MFA setup gera QR Code e secret; verify valida TOTP.
- Senha nunca aparece em logs.
- Rate limit bloqueia após 5 tentativas de login por minuto.