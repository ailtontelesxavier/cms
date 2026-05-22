export interface Permission {
  id: number
  module: string
  action: string
}

export interface Role {
  id: number
  name: string
  description: string | null
  permissions: Permission[]
}

export interface RoleCreate {
  name: string
  description?: string | null
}

export interface RoleUpdate {
  name?: string | null
  description?: string | null
}

export interface PermissionCreate {
  module: string
  action: string
}

export interface RolePermissionUpdate {
  permissions: PermissionCreate[]
}

export interface UserRoleAssign {
  role_ids: number[]
}
