<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { Post, PostStatus } from '@/shared/types/posts'
import { postsApi } from '@/shared/api/posts'
import LoadingSpinner from '@/shared/ui/LoadingSpinner.vue'
import EmptyState from '@/shared/ui/EmptyState.vue'
import ApiError from '@/shared/ui/ApiError.vue'
import PaginationFooter from '@/shared/ui/PaginationFooter.vue'
import { getApiErrorMessage } from '@/shared/api/client'

const router = useRouter()
const posts = ref<Post[]>([])
const total = ref(0)
const page = ref(1)
const statusFilter = ref<PostStatus | ''>('')
const loading = ref(true)
const errorMsg = ref('')

const statusOptions: { value: PostStatus | ''; label: string }[] = [
  { value: '', label: 'Todos' },
  { value: 'draft', label: 'Rascunho' },
  { value: 'review', label: 'Revisão' },
  { value: 'published', label: 'Publicado' },
  { value: 'archived', label: 'Arquivado' },
]

function statusLabel(status: string): string {
  return statusOptions.find(o => o.value === status)?.label || status
}

async function loadPosts() {
  loading.value = true
  errorMsg.value = ''
  try {
    const res = await postsApi.list(page.value, 20, statusFilter.value || undefined)
    posts.value = res.data.items
    total.value = res.data.total
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    loading.value = false
  }
}

async function handlePublish(post: Post) {
  try {
    await postsApi.publish(post.id)
    await loadPosts()
  } catch (err) {
    alert(getApiErrorMessage(err))
  }
}

async function handleArchive(post: Post) {
  try {
    await postsApi.archive(post.id)
    await loadPosts()
  } catch (err) {
    alert(getApiErrorMessage(err))
  }
}

async function handleDelete(post: Post) {
  if (!confirm(`Excluir o post "${post.title}"?`)) return
  try {
    await postsApi.delete(post.id)
    await loadPosts()
  } catch (err) {
    alert(getApiErrorMessage(err))
  }
}

function onStatusChange() {
  page.value = 1
  loadPosts()
}

onMounted(loadPosts)
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-900">Posts</h1>
      <button @click="router.push({ name: 'post-create' })"
        class="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500">
        Novo Post
      </button>
    </div>

    <div class="mb-4 flex gap-2">
      <select v-model="statusFilter" @change="onStatusChange"
        class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500">
        <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
      </select>
    </div>

    <LoadingSpinner v-if="loading" />

    <ApiError v-else-if="errorMsg" :message="errorMsg" @retry="loadPosts" />

    <EmptyState v-else-if="posts.length === 0" />

    <div v-else class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Título</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tags</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Criado em</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="post in posts" :key="post.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ post.title }}</td>
            <td class="px-6 py-4">
              <span
                class="inline-flex rounded-full px-2 py-0.5 text-xs font-medium"
                :class="{
                  'bg-gray-100 text-gray-700': post.status === 'draft',
                  'bg-yellow-100 text-yellow-800': post.status === 'review',
                  'bg-green-100 text-green-800': post.status === 'published',
                  'bg-red-100 text-red-800': post.status === 'archived',
                }">
                {{ statusLabel(post.status) }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">
              {{ post.tags.map(t => t.name).join(', ') || '—' }}
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ new Date(post.created_at).toLocaleDateString('pt-BR') }}</td>
            <td class="px-6 py-4 text-right text-sm">
              <button @click="router.push({ name: 'post-edit', params: { id: post.id } })"
                class="text-sky-600 hover:text-sky-500 mr-2">
                Editar
              </button>
              <button v-if="post.status === 'draft' || post.status === 'review'"
                @click="handlePublish(post)" class="text-green-600 hover:text-green-500 mr-2">
                Publicar
              </button>
              <button v-if="post.status !== 'archived'"
                @click="handleArchive(post)" class="text-amber-600 hover:text-amber-500 mr-2">
                Arquivar
              </button>
              <button @click="handleDelete(post)" class="text-red-600 hover:text-red-500">
                Excluir
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <PaginationFooter
        :page="page"
        :total="total"
        label="post(s)"
        @update:page="page = $event; loadPosts()" />
    </div>
  </div>
</template>
