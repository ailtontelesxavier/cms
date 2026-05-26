import router from '@/app-shell/router'
import { useSessionStore } from '@/auth-session/stores/session'

export async function restoreSessionOrRedirect(): Promise<boolean> {
  const session = useSessionStore()
  const restored = await session.restoreSession()

  if (router.currentRoute.value.meta.requiresAuth && !restored) {
    await router.push({ name: 'login' })
    return false
  }

  return restored
}
