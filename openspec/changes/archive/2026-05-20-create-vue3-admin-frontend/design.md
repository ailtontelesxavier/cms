## Context

The CMS backend already implements authentication, RBAC, tag CRUD, post CRUD, publish/archive actions, and post image upload, but the `frontend/` directory is still empty. The new admin must be introduced as a separate Vue 3 application that consumes `/api/v1` and stays modular enough to evolve with the backend.

The current HTTP contracts are close to what the admin needs, but there are three important gaps: login does not return a `refresh_token` even though `POST /auth/refresh` exists, MFA login does not expose a usable pre-auth challenge for the frontend, and `GET /posts/{id}` returns metadata only instead of the editable HTML payload required by the post editor. The upload contract also needs a stable image identifier that can be reused by download and delete actions.

## Goals / Non-Goals

**Goals:**
- Create the admin foundation in Vue 3 with TypeScript, Composition API, and a modern build toolchain.
- Organize the app around clear modules for shell, auth/session, and content management.
- Support real admin workflows for login, tags, posts, and images with consistent error handling and protected routes.
- Isolate HTTP integration and session state so backend contract changes can be absorbed in one place.

**Non-Goals:**
- Build the public site, SSR flows, or visitor-facing pages.
- Deliver analytics dashboards, user management, or fine-grained permission management in this first change.
- Introduce a full rich text editor in the first iteration; a simpler HTML editing experience is enough initially.
- Redesign backend authentication end to end; this change only includes the minimal backend contract alignment required by the admin.

## Decisions

### 1. Use Vue 3 + Vite + TypeScript + Composition API

The admin will be bootstrapped as a Vue 3 SPA using `<script setup lang="ts">`, Vite for development and builds, and `vue-router` for navigation. This keeps the foundation modern, lightweight, and aligned with current Vue best practices.

Alternatives considered:
- Nuxt would add SSR and full-stack conventions that are unnecessary for this admin surface.
- Options API would increase maintenance cost compared with the standard Vue 3 Composition API approach.

### 2. Organize the frontend by feature modules

Route views should remain thin and compose feature-specific components and composables. The initial structure should separate at least `app-shell`, `auth-session`, and `content-management`, plus a shared layer for API access, common types, and base UI pieces.

Alternatives considered:
- A global type-based layout such as `components`, `views`, and `stores` without feature boundaries is easier to start but becomes harder to maintain as the admin grows.

### 3. Centralize session state in a store backed by session storage

Authenticated state should live in a single store and hydrate from `sessionStorage` so the app survives reloads without keeping tokens around longer than necessary. The store will own the access token, current user, expiration state, and an optional `refresh_token` if the backend starts returning one.

Alternatives considered:
- In-memory only state is safer but forces reauthentication on every reload.
- `localStorage` is more convenient but increases token persistence beyond what this first admin version needs.

### 4. Use a dedicated HTTP client layer

The frontend should wrap backend requests in a shared client with `baseURL` configuration, automatic bearer token injection, and normalized handling for `401`, `403`, `409`, `422`, and network failures. This keeps UI code focused on product behavior instead of raw transport details.

Alternatives considered:
- Calling `fetch` directly inside each screen would reduce dependencies but would duplicate auth and error behavior across the app.

### 5. Treat backend contract gaps as explicit scope

This change should include the minimal backend contract alignment required for the admin to function end to end:
- login/MFA: the backend must expose a workable MFA login handshake or the frontend must explicitly block the flow with a deterministic message.
- refresh: the backend must return `refresh_token` if automatic renewal is a real requirement.
- post editing: the API must return `html`, `summary`, and image metadata when loading a post for editing.
- image lifecycle: upload, download, and delete must share a stable identifier.

Alternatives considered:
- Hiding these gaps behind frontend workarounds would increase complexity and leave fragile flows in place.

### 6. Keep the first editorial iteration operational and narrow

The first admin version should prioritize lists, filters, forms, and the main editorial actions. Post content editing can start with a dedicated HTML editing component, leaving rich text editor integration for a later change once the core contracts are stable.

Alternatives considered:
- Adding a full WYSIWYG editor immediately would raise implementation complexity and introduce extra dependencies before the core admin flows are validated.

## Risks / Trade-offs

- [Browser token storage] -> Mitigation: use `sessionStorage`, avoid long-lived persistence, and keep storage access inside the session store.
- [MFA login depends on backend changes] -> Mitigation: document the dependency in the spec and provide a deterministic blocked state until the contract is extended.
- [Post editing depends on a detailed read contract] -> Mitigation: require a detail payload explicitly before the implementation phase starts.
- [Image contract is inconsistent today] -> Mitigation: require a stable identifier in the spec and validate the backend payload before implementing delete/download UI.
- [No rich text editor in the first delivery] -> Mitigation: isolate the content editor component so it can be swapped later.

## Migration Plan

1. Initialize the Vue 3 project in `frontend/` with scripts, environment configuration, and the base application structure.
2. Implement the app shell, authenticated routing, and shared HTTP client.
3. Integrate session management with login, current-user hydration, and expiration handling.
4. Align the backend contracts needed for MFA, refresh, post detail, and image identifiers.
5. Implement tags, posts, and image workflows on top of the validated contracts.
6. Validate the admin manually against the local backend and add automated frontend tests once the base app is stable.

Rollback: because the frontend does not exist yet, rollback is mainly removing the new app or stopping its deployment. Any backend contract adjustments should be introduced as compatibly as possible.

## Open Questions

- Will the backend start issuing `refresh_token` on login, or should the first admin version rely on reauthentication only?
- Will MFA login use a temporary challenge token, a different verification endpoint, or another handshake strategy?
- Should `GET /posts/{id}` be expanded to return editable content, or should the backend add a dedicated editorial detail endpoint?
- Which field will become the stable image identifier reused by upload, download, and delete flows?