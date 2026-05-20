import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from '@/app-shell/router'
import { useSessionStore } from '@/auth-session/stores/session'
import App from './App.vue'
import './style.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)

async function bootstrap() {
  const session = useSessionStore()
  const restored = await session.restoreSession()

  if (router.currentRoute.value.meta.requiresAuth && !restored) {
    await router.push({ name: 'login' })
  }

  app.mount('#app')
}

bootstrap()
