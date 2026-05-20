<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { Tag } from '@/shared/types/tags'
import { tagsApi } from '@/shared/api/tags'
import LoadingSpinner from '@/shared/ui/LoadingSpinner.vue'
import EmptyState from '@/shared/ui/EmptyState.vue'
import ApiError from '@/shared/ui/ApiError.vue'
import { getApiErrorMessage } from '@/shared/api/client'

const router = useRouter()
const tags = ref<Tag[]>([])
const total = ref(0)
const page = ref(1)
const loading = ref(true)
const errorMsg = ref('')

async function loadTags() {
  loading.value = true
  errorMsg.value = ''
  try {
    const res = await tagsApi.list(page.value, 20)
    tags.value = res.data.items
    total.value = res.data.total
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    loading.value = false
  }
}

async function handleDelete(tag: Tag) {
  if (!confirm(`Excluir a tag "${tag.name}"?`)) return
  try {
    await tagsApi.delete(tag.id)
    await loadTags()
  } catch (err) {
    alert(getApiErrorMessage(err))
  }
}

onMounted(loadTags)
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-900">Tags</h1>
      <button @click="router.push({ name: 'tag-create' })"
        class="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500">
        Nova Tag
      </button>
    </div>

    <LoadingSpinner v-if="loading" />

    <ApiError v-else-if="errorMsg" :message="errorMsg" @retry="loadTags" />

    <EmptyState v-else-if="tags.length === 0" />

    <div v-else class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nome</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Slug</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Descrição</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="tag in tags" :key="tag.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ tag.name }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ tag.slug }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ tag.description || '—' }}</td>
            <td class="px-6 py-4 text-right text-sm">
              <button @click="router.push({ name: 'tag-edit', params: { id: tag.id } })"
                class="text-sky-600 hover:text-sky-500 mr-3">
                Editar
              </button>
              <button @click="handleDelete(tag)" class="text-red-600 hover:text-red-500">
                Excluir
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="total > 20" class="flex items-center justify-between border-t border-gray-200 px-6 py-3">
        <span class="text-sm text-gray-600">{{ total }} tag(s)</span>
        <div class="flex gap-2">
          <button :disabled="page <= 1" @click="page--; loadTags()"
            class="rounded-md border border-gray-300 px-3 py-1 text-sm disabled:opacity-50">
            Anterior
          </button>
          <button :disabled="page * 20 >= total" @click="page++; loadTags()"
            class="rounded-md border border-gray-300 px-3 py-1 text-sm disabled:opacity-50">
            Próximo
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
