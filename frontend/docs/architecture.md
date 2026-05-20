# Frontend Architecture

## Modules

```
src/
  app-shell/          — Global layout, routing, auth guards
  auth-session/       — Authentication, MFA, session state (Pinia)
  content-management/ — Tags CRUD, Posts CRUD, Image upload
  shared/             — HTTP client, types, UI primitives
```

## Key Design Decisions

- **Vue 3 + Composition API** (`<script setup lang="ts">`)
- **Pinia** for state management with `sessionStorage` persistence
- **Axios** wrapped in `shared/api/client.ts` with bearer token injection
- **vue-router** with navigation guards for protected routes
- **Tailwind CSS v4** via `@tailwindcss/vite` plugin (CSS-first config)

## Auth Flow

1. User submits email+password → `POST /auth/token`
2. If MFA enabled (403 `auth:mfa_required`) → user enters TOTP → `POST /auth/mfa/challenge`
3. On success → tokens stored in Pinia + `sessionStorage`
4. On reload → `restoreSession()` rehydrates from storage, validates via `/users/me`
5. If `me()` fails and `refresh_token` exists → `POST /auth/refresh`

## Backend Contracts

| Frontend | Backend Endpoint |
|---|---|
| Login | `POST /api/v1/auth/token` |
| MFA Challenge | `POST /api/v1/auth/mfa/challenge` |
| Refresh | `POST /api/v1/auth/refresh` |
| Current User | `GET /api/v1/users/me` |
| MFA Setup | `POST /api/v1/auth/mfa/setup` |
| MFA Verify | `POST /api/v1/auth/mfa/verify` |
| Tags CRUD | `GET/POST /api/v1/tags`, `PATCH/DELETE /api/v1/tags/{id}` |
| Posts CRUD | `GET/POST /api/v1/posts`, `PATCH/DELETE /api/v1/posts/{id}` |
| Post Detail | `GET /api/v1/posts/{id}/detail` |
| Publish | `POST /api/v1/posts/{id}/publish` |
| Archive | `POST /api/v1/posts/{id}/archive` |
| Image Upload | `POST /api/v1/posts/{id}/images` |
| Image Download | `GET /api/v1/posts/{id}/images/{img_id}/download` |
| Image Delete | `DELETE /api/v1/posts/{id}/images/{img_id}` |
