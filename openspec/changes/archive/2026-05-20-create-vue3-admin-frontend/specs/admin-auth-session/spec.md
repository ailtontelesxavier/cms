## ADDED Requirements

### Requirement: Credential login and session hydration
The system SHALL allow an administrator to authenticate with email and password against the backend, persist the resulting authenticated session in frontend state, and load the current user profile before granting access to protected routes.

#### Scenario: Login succeeds with valid credentials
- **WHEN** an administrator submits valid credentials to the login form
- **THEN** the application stores the returned access token, retrieves the authenticated user profile, and redirects the user to the protected admin area

#### Scenario: Login fails with invalid credentials
- **WHEN** the backend rejects the submitted credentials
- **THEN** the application keeps the user unauthenticated and displays a clear authentication error without losing the submitted form context

### Requirement: Session restoration and expiration handling
The system SHALL restore an existing session from session-scoped storage on page reload, attempt session renewal through `/auth/refresh` when a refresh token is available, and otherwise require reauthentication when the session can no longer be validated.

#### Scenario: Existing session is restored on reload
- **WHEN** the browser reloads while a valid stored session is present
- **THEN** the application rehydrates the session, validates or reloads the current user, and keeps the user inside the protected admin area

#### Scenario: Session expires without refresh support
- **WHEN** a protected request fails because the access token is no longer valid and no usable refresh token is available
- **THEN** the application clears the session and redirects the user back to login

### Requirement: MFA and auth contract edge handling
The system SHALL support MFA setup and verification for authenticated administrators, and SHALL present a deterministic blocking state when the backend signals `auth:mfa_required` during login without providing a usable pre-authentication challenge for verification.

#### Scenario: Authenticated administrator enables MFA
- **WHEN** an authenticated administrator requests MFA setup and confirms a valid verification code
- **THEN** the application completes the setup flow using the backend MFA endpoints and keeps the administrator informed of the result

#### Scenario: Login requires MFA but no challenge contract exists
- **WHEN** the login request is rejected with the backend detail indicating `auth:mfa_required`
- **THEN** the application keeps the session unauthenticated and shows a dedicated message that the backend must provide the MFA login challenge before the flow can continue