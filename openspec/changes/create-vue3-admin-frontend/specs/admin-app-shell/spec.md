## ADDED Requirements

### Requirement: Vue 3 admin application bootstrap
The system SHALL provide a dedicated Vue 3 administrative application under `frontend/` with TypeScript, a standard dev/build toolchain, and environment-based API configuration for the CMS backend.

#### Scenario: Developer starts the admin application locally
- **WHEN** the frontend dependencies are installed and the local development command is executed
- **THEN** the admin application boots successfully and reads the backend base URL from environment configuration

### Requirement: Protected admin route shell
The system SHALL provide an authenticated application shell with route-based navigation for login, posts, tags, and other protected admin views, redirecting unauthenticated users away from private routes.

#### Scenario: Unauthenticated user opens a protected route
- **WHEN** a user without a valid authenticated session navigates directly to a protected admin URL
- **THEN** the application redirects the user to the login route and preserves the intended destination for a future successful login

### Requirement: Shared API client and request state handling
The system SHALL centralize backend communication in a shared API client that attaches the current bearer token when available and exposes consistent loading and error states to route features.

#### Scenario: Authenticated request is sent from an admin screen
- **WHEN** a protected admin feature performs an API request after the session has been established
- **THEN** the request includes the bearer token and the UI receives a normalized success or error result that can be rendered consistently