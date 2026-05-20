<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useSessionStore } from '@/auth-session/stores/session'
import { getApiErrorMessage } from '@/shared/api/client'

const session = useSessionStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const totp = ref('')
const errorMsg = ref('')
const isSubmitting = ref(false)

async function handleSubmit() {
  errorMsg.value = ''
  isSubmitting.value = true

  try {
    await session.mfaChallenge(email.value, password.value, totp.value)
    router.push({ name: 'posts' })
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-50 px-4">
    <div class="w-full max-w-sm">
      <div class="rounded-lg border border-gray-200 bg-white p-8 shadow-sm">
        <h1 class="mb-6 text-center text-2xl font-bold text-gray-900">Autenticação MFA</h1>

        <p class="mb-4 text-sm text-gray-600">
          Esta conta possui autenticação de dois fatores. Informe suas credenciais e o código do seu aplicativo autenticador.
        </p>

        <div v-if="errorMsg"
          class="mb-4 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {{ errorMsg }}
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
            <input id="email" v-model="email" type="email" required autocomplete="email"
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Senha</label>
            <input id="password" v-model="password" type="password" required autocomplete="current-password"
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
          </div>

          <div>
            <label for="totp" class="block text-sm font-medium text-gray-700">Código MFA</label>
            <input id="totp" v-model="totp" type="text" maxlength="6" placeholder="000000" required
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm text-center font-mono tracking-widest shadow-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
          </div>

          <button type="submit" :disabled="isSubmitting || totp.length < 6"
            class="w-full rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-50">
            {{ isSubmitting ? 'Verificando...' : 'Autenticar' }}
          </button>

          <button type="button" @click="router.push({ name: 'login' })"
            class="w-full text-sm text-gray-500 hover:text-gray-700">
            Voltar ao login
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
