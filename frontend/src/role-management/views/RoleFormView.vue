<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { rolesApi } from '@/shared/api/roles'
import LoadingSpinner from '@/shared/ui/LoadingSpinner.vue'
import { getApiErrorMessage } from '@/shared/api/client'

const router = useRouter()
const route = useRoute()

const MODULOS = [
  'administrativo', 'educacional', 'avaliacoes', 'documentos',
  'processos', 'auditoria', 'relatorios',
] as const

const ACOES = [
  'criar', 'ler', 'atualizar', 'excluir',
  'homologar', 'assinar', 'administrar', 'superuser',
] as const

const isEdit = !!route.params.id
const loading = ref(isEdit)
const saving = ref(false)
const errorMsg = ref('')

const form = ref({
  name: '',
  description: '',
})

const permissions = ref<{ module: string; action: string }[]>([])
const selectedModule = ref('')
const selectedAction = ref('')

const availableModules = computed(() =>
  MODULOS.filter(m => !permissions.value.some(p => p.module === m && p.action === 'ler'))
)

const availableActions = computed(() =>
  ACOES.filter(a => !permissions.value.some(p => p.module === selectedModule.value && p.action === a))
)

function addPermission() {
  if (!selectedModule.value || !selectedAction.value) return
  if (permissions.value.some(p => p.module === selectedModule.value && p.action === selectedAction.value)) return
  permissions.value.push({ module: selectedModule.value, action: selectedAction.value })
}

function removePermission(module: string, action: string) {
  permissions.value = permissions.value.filter(p => !(p.module === module && p.action === action))
}

const groupedPermissions = computed(() => {
  const grouped: Record<string, string[]> = {}
  for (const p of permissions.value) {
    if (!grouped[p.module]) grouped[p.module] = []
    grouped[p.module].push(p.action)
  }
  return grouped
})

async function loadRole() {
  if (!route.params.id) return
  loading.value = true
  try {
    const res = await rolesApi.getById(Number(route.params.id))
    const role = res.data
    form.value = { name: role.name, description: role.description || '' }
    permissions.value = role.permissions.map(p => ({ module: p.module, action: p.action }))
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
      const roleRes = await rolesApi.update(Number(route.params.id), {
        name: form.value.name,
        description: form.value.description || null,
      })
      await rolesApi.updatePermissions(roleRes.data.id, {
        permissions: permissions.value,
      })
    } else {
      const roleRes = await rolesApi.create({
        name: form.value.name,
        description: form.value.description || null,
      })
      await rolesApi.updatePermissions(roleRes.data.id, {
        permissions: permissions.value,
      })
    }
    router.push({ name: 'roles' })
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    saving.value = false
  }
}

onMounted(loadRole)
</script>

<template>
  <div class="mx-auto max-w-lg">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">
      {{ isEdit ? 'Editar Perfil' : 'Novo Perfil' }}
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
          <input id="name" v-model="form.name" type="text" required maxlength="100"
            class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
        </div>

        <div>
          <label for="description" class="block text-sm font-medium text-gray-700">Descrição</label>
          <input id="description" v-model="form.description" type="text" maxlength="255"
            class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
        </div>

        <div class="border-t border-gray-200 pt-4">
          <h2 class="text-sm font-medium text-gray-700 mb-3">Permissões</h2>

          <div class="flex gap-2 mb-4 items-end">
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Módulo</label>
              <select v-model="selectedModule"
                class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500">
                <option value="">Selecione...</option>
                <option v-for="m in MODULOS" :key="m" :value="m">{{ m }}</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Ação</label>
              <select v-model="selectedAction"
                class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500">
                <option value="">Selecione...</option>
                <option v-for="a in ACOES" :key="a" :value="a">{{ a }}</option>
              </select>
            </div>
            <button type="button" @click="addPermission" :disabled="!selectedModule || !selectedAction"
              class="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-50">
              Adicionar
            </button>
          </div>

          <div v-if="permissions.length === 0" class="text-sm text-gray-400 italic">
            Nenhuma permissão adicionada
          </div>

          <div v-else class="space-y-2">
            <div v-for="(actions, module) in groupedPermissions" :key="module">
              <h3 class="text-xs font-medium text-gray-500 uppercase mb-1">{{ module }}</h3>
              <div class="flex flex-wrap gap-1 mb-2">
                <span v-for="action in actions" :key="`${module}-${action}`"
                  class="inline-flex items-center gap-1 rounded-full bg-sky-100 px-2 py-0.5 text-xs font-medium text-sky-800">
                  {{ action }}
                  <button type="button" @click="removePermission(module, action)"
                    class="text-sky-600 hover:text-sky-800">&times;</button>
                </span>
              </div>
            </div>
          </div>
        </div>

        <div class="flex gap-3 pt-2">
          <button type="submit" :disabled="saving"
            class="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-50">
            {{ saving ? 'Salvando...' : 'Salvar' }}
          </button>
          <button type="button" @click="router.push({ name: 'roles' })"
            class="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">
            Cancelar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
