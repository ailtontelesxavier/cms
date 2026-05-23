import client from './client'
import type { Role, RoleCreate, RoleUpdate, RolePermissionUpdate } from '@/shared/types/roles'

export const rolesApi = {
  list() {
    return client.get<Role[]>('/roles')
  },

  getEnums() {
    return client.get<{ modulos: string[]; acoes: string[] }>('/roles/enums')
  },

  getById(id: number) {
    return client.get<Role>(`/roles/${id}`)
  },

  create(data: RoleCreate) {
    return client.post<Role>('/roles', data)
  },

  update(id: number, data: RoleUpdate) {
    return client.put<Role>(`/roles/${id}`, data)
  },

  updatePermissions(id: number, data: RolePermissionUpdate) {
    return client.put<Role>(`/roles/${id}/permissions`, data)
  },

  delete(id: number) {
    return client.delete(`/roles/${id}`)
  },
}
