import type { NavigationGuard } from 'vue-router'
import { useSessionStore } from '@/auth-session/stores/session'

export const authGuard: NavigationGuard = (to, _from, next) => {
  const session = useSessionStore()

  if (to.meta.requiresAuth && !session.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.name === 'login' && session.isAuthenticated) {
    next({ name: 'posts' })
  } else {
    next()
  }
}
