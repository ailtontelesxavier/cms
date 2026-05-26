import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from '@/app-shell/router'
import { restoreSessionOrRedirect } from '@/app-shell/guards/session.guard'
import App from './App.vue'
import './style.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)

async function bootstrap() {
  await restoreSessionOrRedirect()
  app.mount('#app')
}

bootstrap()
