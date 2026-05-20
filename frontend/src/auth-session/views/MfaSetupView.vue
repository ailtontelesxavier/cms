<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSessionStore } from '@/auth-session/stores/session'
import LoadingSpinner from '@/shared/ui/LoadingSpinner.vue'
import ApiError from '@/shared/ui/ApiError.vue'
import { getApiErrorMessage } from '@/shared/api/client'

const session = useSessionStore()
const secret = ref('')
const qrcodeSvg = ref('')
const verificationCode = ref('')
const loading = ref(true)
const errorMsg = ref('')
const successMsg = ref('')
const isVerifying = ref(false)

onMounted(() => {
  void setup()
})

async function setup() {
  loading.value = true
  try {
    const data = await session.setupMfa()
    secret.value = data.secret
    qrcodeSvg.value = data.qrcode
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    loading.value = false
  }
}

async function handleVerify() {
  errorMsg.value = ''
  successMsg.value = ''
  isVerifying.value = true

  try {
    await session.verifyMfa(verificationCode.value)
    successMsg.value = 'MFA ativado com sucesso!'
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    isVerifying.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-lg">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Configurar MFA</h1>

    <LoadingSpinner v-if="loading" message="Preparando configuração..." />
    <ApiError v-else-if="errorMsg && !qrcodeSvg" :message="errorMsg" @retry="setup" />

    <template v-else>
      <div v-if="successMsg"
        class="mb-4 rounded-md border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
        {{ successMsg }}
      </div>

      <div class="rounded-lg border border-gray-200 bg-white p-6 space-y-6">
        <div>
          <h2 class="text-sm font-medium text-gray-700 mb-2">
            1. Escaneie o QR Code com seu aplicativo autenticador
          </h2>
          <div v-html="qrcodeSvg" class="flex justify-center" />
        </div>

        <div>
          <h2 class="text-sm font-medium text-gray-700 mb-2">
            2. Ou insira manualmente a chave secreta
          </h2>
          <code class="block rounded bg-gray-100 px-3 py-2 text-sm font-mono break-all">{{ secret }}</code>
        </div>

        <div>
          <h2 class="text-sm font-medium text-gray-700 mb-2">
            3. Digite o código de verificação
          </h2>
          <div v-if="errorMsg && qrcodeSvg"
            class="mb-3 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
            {{ errorMsg }}
          </div>
          <div class="flex gap-3">
            <input v-model="verificationCode" type="text" maxlength="6" placeholder="000000"
              class="block w-32 rounded-md border border-gray-300 px-3 py-2 text-sm text-center font-mono tracking-widest focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
            <button @click="handleVerify" :disabled="isVerifying || verificationCode.length < 6"
              class="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-50">
              {{ isVerifying ? 'Verificando...' : 'Verificar' }}
            </button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
