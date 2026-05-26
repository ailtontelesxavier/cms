import client from './client'
import type { TokenOut, LoginRequest, User, MfaSetupOut, MfaVerifyRequest, MfaChallengeRequest } from '@/shared/types/auth'

export const authApi = {
  login(data: LoginRequest) {
    return client.post<TokenOut>('/auth/token', data)
  },

  refresh(refreshToken: string) {
    return client.post<TokenOut>('/auth/refresh', { refresh_token: refreshToken })
  },

  mfaChallenge(data: MfaChallengeRequest) {
    return client.post<TokenOut>('/auth/mfa/challenge', data)
  },

  me() {
    return client.get<User>('/users/me')
  },

  myPermissions() {
    return client.get<{ module: string; action: string }[]>('/users/me/permissions')
  },

  mfaSetup() {
    return client.post<MfaSetupOut>('/auth/mfa/setup')
  },

  mfaVerify(data: MfaVerifyRequest) {
    return client.post<TokenOut>('/auth/mfa/verify', data)
  },
}
