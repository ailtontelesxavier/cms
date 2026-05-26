import type { NavigationGuard } from 'vue-router'
import { useSessionStore } from '@/auth-session/stores/session'

export const permissionGuard: NavigationGuard = (to, _from, next) => {
  const requiredModule = to.meta.module as string | undefined
  const requiredAction = to.meta.action as string | undefined

  if (requiredModule && requiredAction) {
    const session = useSessionStore()
    if (!session.userHasPermission(requiredModule, requiredAction)) {
      next({ name: 'posts' })
      return
    }
  }

  next()
}
