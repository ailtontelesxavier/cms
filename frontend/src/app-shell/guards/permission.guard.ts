import type { NavigationGuard } from 'vue-router'
import { useSessionStore } from '@/auth-session/stores/session'

function userHasPermission(module: string, action: string): boolean {
  const session = useSessionStore()
  const user = session.currentUser

  if (!user) return false
  if (user.is_superuser) return true

  // TODO: Fetch full permission data from a dedicated endpoint
  // e.g. GET /users/me/permissions returns { module: string, action: string }[]
  // For now, superuser is the only reliable check.
  // Once the endpoint is available, cache permissions in the session store:
  //   return user.permissions?.some(p => p.module === module && p.action === action) ?? false

  return false
}

export const permissionGuard: NavigationGuard = (to, _from, next) => {
  const requiredModule = to.meta.module as string | undefined
  const requiredAction = to.meta.action as string | undefined

  if (requiredModule && requiredAction && !userHasPermission(requiredModule, requiredAction)) {
    next({ name: 'posts' })
  } else {
    next()
  }
}
