<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { Role } from '@/shared/types/roles'
import { rolesApi } from '@/shared/api/roles'
import LoadingSpinner from '@/shared/ui/LoadingSpinner.vue'
import EmptyState from '@/shared/ui/EmptyState.vue'
import ApiError from '@/shared/ui/ApiError.vue'
import { getApiErrorMessage } from '@/shared/api/client'

const router = useRouter()
const roles = ref<Role[]>([])
const loading = ref(true)
const errorMsg = ref('')

async function loadRoles() {
  loading.value = true
  errorMsg.value = ''
  try {
    const res = await rolesApi.list()
    roles.value = res.data
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    loading.value = false
  }
}

async function handleDelete(role: Role) {
  if (!confirm(`Excluir o perfil "${role.name}"?`)) return
  try {
    await rolesApi.delete(role.id)
    await loadRoles()
  } catch (err) {
    alert(getApiErrorMessage(err))
  }
}

onMounted(loadRoles)
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-900">Perfis</h1>
      <button @click="router.push({ name: 'role-create' })"
        class="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500">
        Novo Perfil
      </button>
    </div>

    <LoadingSpinner v-if="loading" />

    <ApiError v-else-if="errorMsg" :message="errorMsg" @retry="loadRoles" />

    <EmptyState v-else-if="roles.length === 0" />

    <div v-else class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nome</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Descrição</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Permissões</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="role in roles" :key="role.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ role.name }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ role.description || '-' }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">
              <div class="flex flex-wrap gap-1">
                <span v-for="perm in role.permissions" :key="perm.id"
                  class="inline-flex items-center rounded-full bg-sky-100 px-2 py-0.5 text-xs font-medium text-sky-800">
                  {{ perm.module }}:{{ perm.action }}
                </span>
                <span v-if="role.permissions.length === 0" class="text-gray-400">Nenhuma</span>
              </div>
            </td>
            <td class="px-6 py-4 text-sm">
              <div class="flex items-center justify-end gap-2">
                <button @click="router.push({ name: 'role-edit', params: { id: role.id } })"
                  class="rounded-md border border-sky-300 px-3 py-1.5 text-sm font-medium text-sky-700 hover:bg-sky-50">
                  Editar
                </button>
                <button @click="handleDelete(role)"
                  class="rounded-md border border-red-300 px-3 py-1.5 text-sm font-medium text-red-700 hover:bg-red-50">
                  Excluir
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
