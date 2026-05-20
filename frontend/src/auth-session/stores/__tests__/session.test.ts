import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useSessionStore, MfaRequiredError } from '../session'
import { authApi } from '@/shared/api/auth'
import { setAuthToken } from '@/shared/api/client'

vi.mock('@/shared/api/auth', () => ({
  authApi: {
    login: vi.fn(),
    refresh: vi.fn(),
    me: vi.fn(),
    mfaChallenge: vi.fn(),
    mfaSetup: vi.fn(),
    mfaVerify: vi.fn(),
  },
}))

vi.mock('@/shared/api/client', () => ({
  setAuthToken: vi.fn(),
  getApiErrorMessage: vi.fn(),
}))

const mockUser = {
  id: '123e4567-e89b-12d3-a456-426614174000',
  email: 'admin@test.com',
  name: 'Admin',
  is_active: true,
  is_superuser: true,
  mfa_enabled: false,
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
  roles: ['admin'],
}

const mockToken = {
  access_token: 'access-token-123',
  refresh_token: 'refresh-token-456',
  token_type: 'bearer',
}

beforeEach(() => {
  setActivePinia(createPinia())
  sessionStorage.clear()
  vi.clearAllMocks()
})

describe('useSessionStore', () => {
  describe('login', () => {
    it('persists session on successful login', async () => {
      vi.mocked(authApi.login).mockResolvedValue({ data: mockToken } as any)
      vi.mocked(authApi.me).mockResolvedValue({ data: mockUser } as any)

      const store = useSessionStore()
      const user = await store.login('admin@test.com', 'password')

      expect(user).toEqual(mockUser)
      expect(store.isAuthenticated).toBe(true)
      expect(store.accessToken).toBe('access-token-123')
      expect(store.refreshToken).toBe('refresh-token-456')
      expect(store.currentUser).toEqual(mockUser)
      expect(setAuthToken).toHaveBeenCalledWith('access-token-123')

      const stored = JSON.parse(sessionStorage.getItem('cms_admin_session')!)
      expect(stored.access_token).toBe('access-token-123')
      expect(stored.refresh_token).toBe('refresh-token-456')
      expect(stored.user).toEqual(mockUser)
    })

    it('throws MfaRequiredError when backend returns 403 mfa_required', async () => {
      const error = { response: { data: { detail: 'auth:mfa_required' } } }
      vi.mocked(authApi.login).mockRejectedValue(error)

      const store = useSessionStore()
      await expect(store.login('admin@test.com', 'password')).rejects.toThrow(MfaRequiredError)
      expect(store.isAuthenticated).toBe(false)
    })

    it('sets error on failed login', async () => {
      const error = { response: { data: { detail: 'Invalid credentials' } } }
      vi.mocked(authApi.login).mockRejectedValue(error)

      const store = useSessionStore()
      await expect(store.login('wrong@test.com', 'wrong')).rejects.toThrow()
      expect(store.error).toBe('Invalid credentials')
    })
  })

  describe('mfaChallenge', () => {
    it('authenticates with valid MFA code', async () => {
      vi.mocked(authApi.mfaChallenge).mockResolvedValue({ data: mockToken } as any)
      vi.mocked(authApi.me).mockResolvedValue({ data: mockUser } as any)

      const store = useSessionStore()
      const user = await store.mfaChallenge('admin@test.com', 'password', '123456')

      expect(user).toEqual(mockUser)
      expect(store.isAuthenticated).toBe(true)
      expect(store.accessToken).toBe('access-token-123')
    })

    it('rejects invalid MFA code', async () => {
      vi.mocked(authApi.mfaChallenge).mockRejectedValue(new Error('Invalid MFA token'))

      const store = useSessionStore()
      await expect(store.mfaChallenge('admin@test.com', 'password', '000000')).rejects.toThrow()
      expect(store.isAuthenticated).toBe(false)
    })
  })

  describe('restoreSession', () => {
    it('restores valid session from storage', async () => {
      sessionStorage.setItem('cms_admin_session', JSON.stringify({
        access_token: 'stored-token',
        refresh_token: 'stored-refresh',
        user: mockUser,
      }))
      vi.mocked(authApi.me).mockResolvedValue({ data: mockUser } as any)

      const store = useSessionStore()
      const result = await store.restoreSession()

      expect(result).toBe(true)
      expect(store.accessToken).toBe('stored-token')
      expect(store.refreshToken).toBe('stored-refresh')
      expect(store.currentUser).toEqual(mockUser)
    })

    it('clears session when me() fails and no refresh token', async () => {
      sessionStorage.setItem('cms_admin_session', JSON.stringify({
        access_token: 'expired-token',
        refresh_token: null,
        user: mockUser,
      }))
      vi.mocked(authApi.me).mockRejectedValue(new Error('expired'))

      const store = useSessionStore()
      const result = await store.restoreSession()

      expect(result).toBe(false)
      expect(store.isAuthenticated).toBe(false)
      expect(sessionStorage.getItem('cms_admin_session')).toBeNull()
    })

    it('tries refresh when me() fails and refresh token exists', async () => {
      sessionStorage.setItem('cms_admin_session', JSON.stringify({
        access_token: 'expired-token',
        refresh_token: 'valid-refresh',
        user: mockUser,
      }))
      vi.mocked(authApi.me).mockRejectedValueOnce(new Error('expired'))
      vi.mocked(authApi.refresh).mockResolvedValue({ data: mockToken } as any)
      vi.mocked(authApi.me).mockResolvedValueOnce({ data: mockUser } as any)

      const store = useSessionStore()
      const result = await store.restoreSession()

      expect(result).toBe(true)
      expect(authApi.refresh).toHaveBeenCalledWith('valid-refresh')
      expect(store.accessToken).toBe('access-token-123')
    })
  })

  describe('clearSession', () => {
    it('clears all session data', () => {
      sessionStorage.setItem('cms_admin_session', JSON.stringify({
        access_token: 'token', refresh_token: 'refresh', user: mockUser,
      }))

      const store = useSessionStore()
      store.accessToken = 'token'
      store.refreshToken = 'refresh'
      store.currentUser = mockUser

      store.clearSession()

      expect(store.accessToken).toBeNull()
      expect(store.refreshToken).toBeNull()
      expect(store.currentUser).toBeNull()
      expect(store.isAuthenticated).toBe(false)
      expect(sessionStorage.getItem('cms_admin_session')).toBeNull()
    })
  })
})
