<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSessionStore, MfaRequiredError } from '@/auth-session/stores/session'
import { getApiErrorMessage } from '@/shared/api/client'

const session = useSessionStore()
const router = useRouter()
const route = useRoute()

const email = ref('')
const password = ref('')
const totp = ref('')
const errorMsg = ref('')
const isSubmitting = ref(false)
const mfaRequired = ref(false)

async function handleSubmit() {
  errorMsg.value = ''
  isSubmitting.value = true

  try {
    if (mfaRequired.value || totp.value) {
      await session.mfaChallenge(email.value, password.value, totp.value)
    } else {
      await session.login(email.value, password.value)
    }
    const redirect = (route.query.redirect as string) || '/'
    router.push(redirect)
  } catch (err: unknown) {
    if (err instanceof MfaRequiredError) {
      mfaRequired.value = true
      return
    }
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
        <h1 class="mb-6 text-center text-2xl font-bold text-gray-900">CMS Admin</h1>

        <div v-if="mfaRequired" class="mb-4 rounded-md border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-700">
          Esta conta possui autenticação de dois fatores. Digite o código do seu aplicativo autenticador.
        </div>

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
            <input id="totp" v-model="totp" type="text" maxlength="6" placeholder="000000"
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm text-center font-mono tracking-widest shadow-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
          </div>

          <button type="submit" :disabled="isSubmitting"
            class="w-full rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-50">
            {{ isSubmitting ? 'Entrando...' : mfaRequired ? 'Verificar código' : 'Entrar' }}
          </button>

          <button v-if="mfaRequired" type="button" @click="mfaRequired = false"
            class="w-full text-sm text-gray-500 hover:text-gray-700">
            Voltar
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
