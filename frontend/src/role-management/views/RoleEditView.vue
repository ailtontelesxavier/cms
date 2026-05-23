<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { rolesApi } from '@/shared/api/roles'
import LoadingSpinner from '@/shared/ui/LoadingSpinner.vue'
import { getApiErrorMessage } from '@/shared/api/client'

const router = useRouter()
const route = useRoute()

const FALLBACK_MODULOS = [
  'permissao', 'administrativo', 'auth', 'posts',
  'documentos', 'processos', 'auditoria', 'relatorios',
]

const FALLBACK_ACOES = [
  'criar', 'ler', 'atualizar', 'excluir',
  'assinar', 'administrar', 'relatorios',
]

const modulos = ref<string[]>([])
const acoes = ref<string[]>([])
const enumsLoading = ref(true)
const loading = ref(true)
const saving = ref(false)
const errorMsg = ref('')

const form = ref({
  name: '',
  description: '',
})

const permissions = ref<{ module: string; action: string }[]>([])
const selectedModule = ref('')
const selectedActions = ref<string[]>([])

async function loadEnums() {
  try {
    const res = await rolesApi.getEnums()
    modulos.value = res.data.modulos
    acoes.value = res.data.acoes
  } catch {
    modulos.value = FALLBACK_MODULOS
    acoes.value = FALLBACK_ACOES
  } finally {
    enumsLoading.value = false
  }
}

function onModuleChange() {
  selectedActions.value = []
}

function toggleAction(action: string) {
  const idx = selectedActions.value.indexOf(action)
  if (idx >= 0) {
    selectedActions.value = selectedActions.value.filter(a => a !== action)
  } else {
    selectedActions.value = [...selectedActions.value, action]
  }
}

function addModule() {
  if (!selectedModule.value || selectedActions.value.length === 0) return
  for (const action of selectedActions.value) {
    if (!permissions.value.some(p => p.module === selectedModule.value && p.action === action)) {
      permissions.value.push({ module: selectedModule.value, action })
    }
  }
  selectedModule.value = ''
  selectedActions.value = []
}

function removeModule(module: string) {
  permissions.value = permissions.value.filter(p => p.module !== module)
}

const groupedPermissions = computed(() => {
  const grouped: Record<string, string[]> = {}
  for (const p of permissions.value) {
    if (!grouped[p.module]) grouped[p.module] = []
    if (!grouped[p.module].includes(p.action)) {
      grouped[p.module].push(p.action)
    }
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
    await rolesApi.update(Number(route.params.id), {
      name: form.value.name,
      description: form.value.description || null,
    })
    await rolesApi.updatePermissions(Number(route.params.id), {
      permissions: permissions.value,
    })
    router.push({ name: 'roles' })
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  await Promise.all([loadEnums(), loadRole()])
})
</script>

<template>
  <div class="mx-auto max-w-lg">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Editar Perfil</h1>

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

          <div class="space-y-3 mb-4 rounded-lg border border-gray-200 bg-gray-50 p-4">
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Módulo</label>
              <div v-if="enumsLoading" class="text-xs text-gray-400 italic">Carregando módulos...</div>
              <select v-else v-model="selectedModule" @change="onModuleChange"
                class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500">
                <option value="">Selecione um módulo...</option>
                <option v-for="m in modulos" :key="m" :value="m">{{ m }}</option>
              </select>
            </div>

            <div v-if="selectedModule">
              <label class="block text-xs font-medium text-gray-500 mb-1">Ações</label>
              <div class="grid grid-cols-2 gap-1">
                <label v-for="action in acoes" :key="action"
                  class="flex items-center gap-2 rounded px-2 py-1 cursor-pointer hover:bg-white">
                  <input type="checkbox" :value="action" :checked="selectedActions.includes(action)"
                    @change="toggleAction(action)"
                    class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
                  <span class="text-sm text-gray-700">{{ action }}</span>
                </label>
              </div>
            </div>

            <button type="button" @click="addModule"
              :disabled="!selectedModule || selectedActions.length === 0"
              class="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-50">
              Adicionar Módulo
            </button>
          </div>

          <div v-if="Object.keys(groupedPermissions).length === 0" class="text-sm text-gray-400 italic">
            Nenhuma permissão adicionada
          </div>

          <div v-else class="space-y-2">
            <div v-for="(actions, module) in groupedPermissions" :key="module"
              class="rounded-lg border border-gray-200 p-3">
              <div class="flex items-center justify-between mb-1">
                <h3 class="text-xs font-medium text-gray-500 uppercase">{{ module }}</h3>
                <button type="button" @click="removeModule(module)"
                  class="text-red-400 hover:text-red-600 text-sm leading-none">&times;</button>
              </div>
              <div class="flex flex-wrap gap-1">
                <span v-for="action in actions" :key="`${module}-${action}`"
                  class="inline-flex items-center rounded-full bg-sky-100 px-2 py-0.5 text-xs font-medium text-sky-800">
                  {{ action }}
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
