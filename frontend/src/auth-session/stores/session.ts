import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/shared/types/auth'
import { authApi } from '@/shared/api/auth'
import { setAuthToken } from '@/shared/api/client'

const STORAGE_KEY = 'cms_admin_session'

interface SessionData {
  access_token: string
  refresh_token?: string | null
  user: User
}

function getErrorDetail(err: unknown): string | undefined {
  const responseDetail = (err as { response?: { data?: { detail?: unknown } } })?.response?.data?.detail
  if (typeof responseDetail === 'string') return responseDetail
  if (err instanceof Error) return err.message
  return undefined
}

function isMfaRequiredError(err: unknown): boolean {
  return getErrorDetail(err)?.includes('auth:mfa_required') ?? false
}

export const useSessionStore = defineStore('session', () => {
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const currentUser = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!accessToken.value && !!currentUser.value)

  function persistSession(token: string, user: User, rToken?: string | null) {
    accessToken.value = token
    refreshToken.value = rToken || null
    currentUser.value = user
    setAuthToken(token)
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
      access_token: token,
      refresh_token: rToken || null,
      user,
    }))
  }

  function restoreFromStorage(): SessionData | null {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    try {
      return JSON.parse(raw) as SessionData
    } catch {
      sessionStorage.removeItem(STORAGE_KEY)
      return null
    }
  }

  async function login(email: string, password: string) {
    loading.value = true
    error.value = null

    try {
      const tokenRes = await authApi.login({ email, password })
      const { access_token, refresh_token } = tokenRes.data

      setAuthToken(access_token)
      const userRes = await authApi.me()
      const user = userRes.data

      persistSession(access_token, user, refresh_token)
      return user
    } catch (err: unknown) {
      const detail = getErrorDetail(err)
      if (isMfaRequiredError(err)) {
        throw new MfaRequiredError(email, password)
      }
      error.value = detail || 'Falha na autenticação'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function mfaChallenge(email: string, password: string, totp: string) {
    loading.value = true
    error.value = null

    try {
      const res = await authApi.mfaChallenge({ email, password, totp })
      const { access_token, refresh_token } = res.data

      setAuthToken(access_token)
      const userRes = await authApi.me()
      const user = userRes.data

      persistSession(access_token, user, refresh_token)
      return user
    } catch (err: unknown) {
      error.value = 'Código MFA inválido'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function restoreSession() {
    const saved = restoreFromStorage()
    if (!saved) return false

    accessToken.value = saved.access_token
    refreshToken.value = saved.refresh_token || null
    currentUser.value = saved.user
    setAuthToken(saved.access_token)

    try {
      const userRes = await authApi.me()
      currentUser.value = userRes.data
      persistSession(saved.access_token, userRes.data, saved.refresh_token)
      return true
    } catch {
      if (saved.refresh_token) {
        return refreshSession()
      }
      clearSession()
      return false
    }
  }

  function clearSession() {
    accessToken.value = null
    refreshToken.value = null
    currentUser.value = null
    setAuthToken(null)
    sessionStorage.removeItem(STORAGE_KEY)
  }

  async function refreshSession() {
    if (!refreshToken.value) {
      clearSession()
      return false
    }

    try {
      const res = await authApi.refresh(refreshToken.value)
      const { access_token, refresh_token } = res.data
      setAuthToken(access_token)
      const userRes = await authApi.me()
      persistSession(access_token, userRes.data, refresh_token)
      return true
    } catch {
      clearSession()
      return false
    }
  }

  async function setupMfa() {
    const res = await authApi.mfaSetup()
    return res.data
  }

  async function verifyMfa(token: string) {
    const res = await authApi.mfaVerify({ token })
    const { access_token, refresh_token } = res.data
    setAuthToken(access_token)
    const userRes = await authApi.me()
    persistSession(access_token, userRes.data, refresh_token)
  }

  return {
    accessToken,
    refreshToken,
    currentUser,
    loading,
    error,
    isAuthenticated,
    login,
    mfaChallenge,
    restoreSession,
    refreshSession,
    clearSession,
    setupMfa,
    verifyMfa,
  }
})

export class MfaRequiredError extends Error {
  email: string
  password: string

  constructor(email: string, password: string) {
    super('auth:mfa_required')
    this.email = email
    this.password = password
    this.name = 'MfaRequiredError'
  }
}
