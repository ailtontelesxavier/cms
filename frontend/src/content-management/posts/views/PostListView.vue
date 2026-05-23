<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { Post, PostStatus } from '@/shared/types/posts'
import { postsApi } from '@/shared/api/posts'
import LoadingSpinner from '@/shared/ui/LoadingSpinner.vue'
import EmptyState from '@/shared/ui/EmptyState.vue'
import ApiError from '@/shared/ui/ApiError.vue'
import PaginationFooter from '@/shared/ui/PaginationFooter.vue'
import ConfirmDialog from '@/shared/ui/ConfirmDialog.vue'
import { getApiErrorMessage } from '@/shared/api/client'

const router = useRouter()
const posts = ref<Post[]>([])
const total = ref(0)
const page = ref(1)
const statusFilter = ref<PostStatus | ''>('')
const searchQuery = ref('')
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
    const res = await postsApi.list(page.value, 20, statusFilter.value || undefined, searchQuery.value || undefined)
    posts.value = res.data.items
    total.value = res.data.total
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    loading.value = false
  }
}

const dialog = ref({
  open: false,
  title: '',
  message: '',
  confirmLabel: '',
  confirmClass: '',
  action: '' as 'publish' | 'archive' | 'delete',
  post: null as Post | null,
  loading: false,
})

function openDialog(action: 'publish' | 'archive' | 'delete', post: Post) {
  const config = {
    publish: { title: 'Publicar Post', confirmLabel: 'Publicar', confirmClass: 'rounded-md bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-500 disabled:opacity-50' },
    archive: { title: 'Arquivar Post', confirmLabel: 'Arquivar', confirmClass: 'rounded-md bg-amber-600 px-4 py-2 text-sm font-medium text-white hover:bg-amber-500 disabled:opacity-50' },
    delete: { title: 'Excluir Post', confirmLabel: 'Excluir', confirmClass: 'rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-500 disabled:opacity-50' },
  }
  const c = config[action]
  dialog.value = {
    open: true,
    title: c.title,
    message: action === 'delete'
      ? `Excluir o post "${post.title}"? Esta ação não pode ser desfeita.`
      : `${c.title} "${post.title}"?`,
    confirmLabel: c.confirmLabel,
    confirmClass: c.confirmClass,
    action,
    post,
    loading: false,
  }
}

async function handleConfirm() {
  if (!dialog.value.post) return
  dialog.value.loading = true
  try {
    if (dialog.value.action === 'publish') {
      await postsApi.publish(dialog.value.post.id)
    } else if (dialog.value.action === 'archive') {
      await postsApi.archive(dialog.value.post.id)
    } else if (dialog.value.action === 'delete') {
      await postsApi.delete(dialog.value.post.id)
    }
    dialog.value.open = false
    await loadPosts()
  } catch (err) {
    dialog.value.loading = false
    dialog.value.open = false
    alert(getApiErrorMessage(err))
  }
}

function onStatusChange() {
  page.value = 1
  void loadPosts()
}

function onSearch() {
  page.value = 1
  void loadPosts()
}

onMounted(() => void loadPosts())
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
      <input v-model="searchQuery" type="text" placeholder="Buscar por título..." @keyup.enter="onSearch"
        class="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
      <button @click="onSearch"
        class="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500">
        Buscar
      </button>
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
            <td class="px-6 py-4 text-sm">
              <div class="flex items-center justify-end gap-2">
                <button @click="router.push({ name: 'post-edit', params: { id: post.id } })"
                  class="rounded-md border border-sky-300 px-3 py-1.5 text-sm font-medium text-sky-700 hover:bg-sky-50">
                  Editar
                </button>
                <button v-if="post.status === 'draft' || post.status === 'review'"
                  @click="openDialog('publish', post)"
                  class="rounded-md border border-green-300 px-3 py-1.5 text-sm font-medium text-green-700 hover:bg-green-50">
                  Publicar
                </button>
                <button v-if="post.status !== 'archived'"
                  @click="openDialog('archive', post)"
                  class="rounded-md border border-amber-300 px-3 py-1.5 text-sm font-medium text-amber-700 hover:bg-amber-50">
                  Arquivar
                </button>
                <button @click="openDialog('delete', post)"
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
        label="post(s)"
        @update:page="page = $event; loadPosts()" />
    </div>

    <ConfirmDialog
      :open="dialog.open"
      :title="dialog.title"
      :message="dialog.message"
      :confirm-label="dialog.confirmLabel"
      :confirm-class="dialog.confirmClass"
      :loading="dialog.loading"
      @confirm="handleConfirm"
      @cancel="dialog.open = false"
    />
  </div>
</template>
