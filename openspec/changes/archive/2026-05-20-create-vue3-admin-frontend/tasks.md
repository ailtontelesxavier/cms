## 1. Frontend bootstrap

- [x] 1.1 Initialize the Vue 3 + TypeScript admin project under `frontend/` with Vite, package scripts, and environment-based API configuration.
- [x] 1.2 Establish the base frontend structure for feature modules, shared UI primitives, shared types, and application entrypoints.
- [x] 1.3 Add the core frontend dependencies for routing, state management, and HTTP integration, and confirm the app boots locally.

## 2. App shell and shared infrastructure

- [x] 2.1 Implement the global app shell with router setup, public login route, and protected admin route groups.
- [x] 2.2 Create the shared API client with base URL configuration, bearer token injection, and normalized handling for 401, 403, 409, 422, and network errors.
- [x] 2.3 Add reusable loading, empty-state, and API error presentation patterns that can be consumed by admin features.

## 3. Auth and session flows

- [x] 3.1 Implement the session store with access-token persistence in `sessionStorage`, current-user hydration, and logout behavior.
- [x] 3.2 Build the login screen and successful credential-login flow using `/auth/token` and `/users/me`.
- [x] 3.3 Implement session restoration on reload and fallback expiration handling when no usable refresh token is available.
- [x] 3.4 Add MFA setup and verification screens for authenticated administrators and a dedicated blocked state for `auth:mfa_required` login responses.

## 4. Backend contract alignment

- [x] 4.1 Align the backend auth contract for the admin by deciding whether login returns `refresh_token` and how MFA login challenges are represented.
- [x] 4.2 Align the backend post detail contract so the admin can load editable HTML, summary, tags, and image metadata for an existing post.
- [x] 4.3 Align the backend upload contract so image upload, download, and delete operations use the same stable image identifier.

## 5. Content management features

- [x] 5.1 Implement tag listing, creation, update, and deletion flows with paginated state and API validation feedback.
- [x] 5.2 Implement post listing with status filtering and row actions for edit, publish, archive, and delete.
- [x] 5.3 Implement post create and edit flows with fields for title, slug, summary, HTML content, and tag assignment.
- [x] 5.4 Implement post image upload and removal flows inside the post editing experience using the aligned backend image contract.

## 6. Validation and delivery

- [x] 6.1 Run the frontend against the local backend to validate login, tags, posts, publish/archive, and image workflows end to end.
- [x] 6.2 Add automated frontend tests for the session store, protected routing, and the primary content-management flows.
- [x] 6.3 Document local setup, required environment variables, and any backend contract assumptions needed to run the admin project.