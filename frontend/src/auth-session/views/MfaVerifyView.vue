<script setup lang="ts">
import { ref } from 'vue'
import { useSessionStore } from '@/auth-session/stores/session'
import { useRouter } from 'vue-router'
import { getApiErrorMessage } from '@/shared/api/client'

const session = useSessionStore()
const router = useRouter()
const code = ref('')
const errorMsg = ref('')
const isSubmitting = ref(false)

async function handleVerify() {
  errorMsg.value = ''
  isSubmitting.value = true

  try {
    await session.verifyMfa(code.value)
    router.push({ name: 'posts' })
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-sm">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Verificação MFA</h1>

    <div v-if="errorMsg"
      class="mb-4 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <form @submit.prevent="handleVerify" class="rounded-lg border border-gray-200 bg-white p-6 space-y-4">
      <p class="text-sm text-gray-600">
        Digite o código de 6 dígitos do seu aplicativo autenticador.
      </p>

      <div>
        <label for="mfa-code" class="block text-sm font-medium text-gray-700">Código</label>
        <input id="mfa-code" v-model="code" type="text" maxlength="6" placeholder="000000" required
          class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm text-center font-mono tracking-widest focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
      </div>

      <button type="submit" :disabled="isSubmitting || code.length < 6"
        class="w-full rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-50">
        {{ isSubmitting ? 'Verificando...' : 'Verificar' }}
      </button>
    </form>
  </div>
</template>
