import type { NavigationGuard } from 'vue-router'
import { useSessionStore } from '@/auth-session/stores/session'

export const mfaGuard: NavigationGuard = (to, _from, next) => {
  const session = useSessionStore()

  if (to.meta.requiresMfa && session.currentUser && !session.currentUser.mfa_enabled) {
    next({ name: 'mfa-setup' })
  } else {
    next()
  }
}
