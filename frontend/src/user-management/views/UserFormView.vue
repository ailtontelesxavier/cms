<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usersApi } from '@/shared/api/users'
import LoadingSpinner from '@/shared/ui/LoadingSpinner.vue'
import { getApiErrorMessage } from '@/shared/api/client'

const router = useRouter()
const route = useRoute()

const isEdit = !!route.params.id
const loading = ref(isEdit)
const saving = ref(false)
const errorMsg = ref('')

const form = ref({
  name: '',
  email: '',
  password: '',
  is_active: true,
})

async function loadUser() {
  if (!route.params.id) return
  loading.value = true
  try {
    const res = await usersApi.getById(route.params.id as string)
    const user = res.data
    form.value = { name: user.name, email: user.email, password: '', is_active: user.is_active }
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  saving.value = true
  errorMsg.value = ''

  try {
    if (isEdit) {
      await usersApi.update(route.params.id as string, {
        name: form.value.name,
        is_active: form.value.is_active,
      })
    } else {
      await usersApi.create({
        name: form.value.name,
        email: form.value.email,
        password: form.value.password,
      })
    }
    router.push({ name: 'users' })
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    saving.value = false
  }
}

onMounted(loadUser)
</script>

<template>
  <div class="mx-auto max-w-lg">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">
      {{ isEdit ? 'Editar Usuário' : 'Novo Usuário' }}
    </h1>

    <LoadingSpinner v-if="loading" />

    <div v-else class="rounded-lg border border-gray-200 bg-white p-6">
      <div v-if="errorMsg"
        class="mb-4 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
        {{ errorMsg }}
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700">Nome</label>
          <input id="name" v-model="form.name" type="text" required maxlength="255"
            class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
        </div>

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input id="email" v-model="form.email" type="email" required maxlength="255" :disabled="isEdit"
            class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500 disabled:bg-gray-100 disabled:text-gray-500" />
        </div>

        <div v-if="!isEdit">
          <label for="password" class="block text-sm font-medium text-gray-700">Senha</label>
          <input id="password" v-model="form.password" type="password" required minlength="8"
            class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
        </div>

        <div v-if="isEdit">
          <label class="flex items-center gap-2">
            <input v-model="form.is_active" type="checkbox"
              class="rounded border-gray-300 text-sky-600 focus:ring-sky-500" />
            <span class="text-sm font-medium text-gray-700">Usuário ativo</span>
          </label>
        </div>

        <div class="flex gap-3 pt-2">
          <button type="submit" :disabled="saving"
            class="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-50">
            {{ saving ? 'Salvando...' : 'Salvar' }}
          </button>
          <button type="button" @click="router.push({ name: 'users' })"
            class="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">
            Cancelar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
