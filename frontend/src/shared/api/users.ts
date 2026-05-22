import client from './client'
import type { PaginatedResult } from '@/shared/types/api'
import type { User, MfaSetupOut, MfaInfoOut } from '@/shared/types/auth'

export const usersApi = {
  list(page = 1, pageSize = 20, q?: string) {
    return client.get<PaginatedResult<User>>('/users', {
      params: { page, page_size: pageSize, ...(q ? { q } : {}) },
    })
  },

  getById(id: string) {
    return client.get<User>(`/users/${id}`)
  },

  create(data: { email: string; name: string; password: string }) {
    return client.post<User>('/users', data)
  },

  update(id: string, data: { name?: string; is_active?: boolean }) {
    return client.patch<User>(`/users/${id}`, data)
  },

  updatePassword(id: string, data: { password: string }) {
    return client.patch(`/users/${id}/password`, data)
  },

  delete(id: string) {
    return client.delete(`/users/${id}`)
  },

  getMfa(userId: string) {
    return client.get<MfaInfoOut>(`/users/${userId}/mfa`)
  },

  setupMfa(userId: string) {
    return client.post<MfaSetupOut>(`/users/${userId}/mfa/setup`)
  },

  verifyMfa(userId: string, token: string) {
    return client.post(`/users/${userId}/mfa/verify`, { token })
  },
}
