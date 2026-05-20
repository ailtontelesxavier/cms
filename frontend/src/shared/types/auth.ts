export interface User {
  id: string
  email: string
  name: string
  is_active: boolean
  is_superuser: boolean
  mfa_enabled: boolean
  created_at: string
  updated_at: string
  roles: string[]
}

export interface TokenOut {
  access_token: string
  refresh_token?: string | null
  token_type: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface MfaChallengeRequest {
  email: string
  password: string
  totp: string
}

export interface MfaSetupOut {
  secret: string
  qrcode: string
}

export interface MfaVerifyRequest {
  token: string
}
