<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { User } from '@/shared/types/auth'
import { usersApi } from '@/shared/api/users'
import LoadingSpinner from '@/shared/ui/LoadingSpinner.vue'
import EmptyState from '@/shared/ui/EmptyState.vue'
import ApiError from '@/shared/ui/ApiError.vue'
import PaginationFooter from '@/shared/ui/PaginationFooter.vue'
import { getApiErrorMessage } from '@/shared/api/client'

const router = useRouter()
const users = ref<User[]>([])
const total = ref(0)
const page = ref(1)
const searchQuery = ref('')
const loading = ref(true)
const errorMsg = ref('')

async function loadUsers() {
  loading.value = true
  errorMsg.value = ''
  try {
    const res = await usersApi.list(page.value, 20, searchQuery.value || undefined)
    users.value = res.data.items
    total.value = res.data.total
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    loading.value = false
  }
}

function onSearch() {
  page.value = 1
  void loadUsers()
}

async function handleDelete(user: User) {
  if (!confirm(`Excluir o usuário "${user.name}"?`)) return
  try {
    await usersApi.delete(user.id)
    await loadUsers()
  } catch (err) {
    alert(getApiErrorMessage(err))
  }
}

onMounted(loadUsers)
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-900">Usuários</h1>
      <button @click="router.push({ name: 'user-create' })"
        class="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500">
        Novo Usuário
      </button>
    </div>

    <div class="mb-4 flex gap-2">
      <input v-model="searchQuery" type="text" placeholder="Buscar por nome ou email..." @keyup.enter="onSearch"
        class="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
      <button @click="onSearch"
        class="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500">
        Buscar
      </button>
    </div>

    <LoadingSpinner v-if="loading" />

    <ApiError v-else-if="errorMsg" :message="errorMsg" @retry="loadUsers" />

    <EmptyState v-else-if="users.length === 0" />

    <div v-else class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nome</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ativo</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">MFA</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Criado em</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ user.name }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ user.email }}</td>
            <td class="px-6 py-4">
              <span
                class="inline-flex rounded-full px-2 py-0.5 text-xs font-medium"
                :class="user.is_active
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'">
                {{ user.is_active ? 'Sim' : 'Não' }}
              </span>
            </td>
            <td class="px-6 py-4">
              <span
                class="inline-flex rounded-full px-2 py-0.5 text-xs font-medium"
                :class="user.mfa_enabled
                  ? 'bg-green-100 text-green-800'
                  : 'bg-gray-100 text-gray-700'">
                {{ user.mfa_enabled ? 'Ativo' : 'Inativo' }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ new Date(user.created_at).toLocaleDateString('pt-BR') }}</td>
            <td class="px-6 py-4 text-sm">
              <div class="flex items-center justify-end gap-2">
                <button @click="router.push({ name: 'user-edit', params: { id: user.id } })"
                  class="rounded-md border border-sky-300 px-3 py-1.5 text-sm font-medium text-sky-700 hover:bg-sky-50">
                  Editar
                </button>
                <button @click="handleDelete(user)"
                  class="rounded-md border border-red-300 px-3 py-1.5 text-sm font-medium text-red-700 hover:bg-red-50">
                  Excluir
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <PaginationFooter
        :page="page"
        :total="total"
        label="usuário(s)"
        @update:page="page = $event; loadUsers()" />
    </div>
  </div>
</template>
