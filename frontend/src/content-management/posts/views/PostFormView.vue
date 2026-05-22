<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { postsApi } from '@/shared/api/posts'
import LoadingSpinner from '@/shared/ui/LoadingSpinner.vue'
import { getApiErrorMessage } from '@/shared/api/client'
import ImageUploader from '@/content-management/images/components/ImageUploader.vue'
import EditorBlock from '@/content-management/posts/components/EditorBlock.vue'

const router = useRouter()
const route = useRoute()

const isEdit = !!route.params.id
const loading = ref(isEdit)
const saving = ref(false)
const errorMsg = ref('')
const postId = ref(route.params.id as string | undefined)

const form = ref({
  title: '',
  slug: '',
  html: '',
  summary: '',
  tagIds: [] as number[],
})

const availableTags = ref<{ id: number; name: string }[]>([])
const editorRef = ref<InstanceType<typeof EditorBlock>>()

async function loadPost() {
  if (!postId.value) return
  loading.value = true
  try {
    const res = await postsApi.getPostDetail(postId.value)
    const post = res.data
    form.value.title = post.title
    form.value.slug = post.slug
    form.value.tagIds = post.tags.map(t => t.id)
    form.value.summary = post?.content?.summary || ''
    form.value.html = post?.content?.html || ''
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    loading.value = false
  }
}

async function loadTags() {
  try {
    const { tagsApi } = await import('@/shared/api/tags')
    const res = await tagsApi.list(1, 100)
    availableTags.value = res.data.items.map(t => ({ id: t.id, name: t.name }))
  } catch {
  }
}

async function handleSubmit() {
  saving.value = true
  errorMsg.value = ''

  await editorRef.value?.handleSave()

  try {
    if (isEdit && postId.value) {
      await postsApi.update(postId.value, {
        title: form.value.title,
        html: form.value.html || undefined,
        summary: form.value.summary || undefined,
        tag_ids: form.value.tagIds.length > 0 ? form.value.tagIds : undefined,
      })
    } else {
      const res = await postsApi.create({
        title: form.value.title,
        html: form.value.html || '<p></p>',
        summary: form.value.summary,
        tag_ids: form.value.tagIds,
      })
      postId.value = res.data.id
    }
    router.push({ name: 'posts' })
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    saving.value = false
  }
}

function toggleTag(tagId: number) {
  const idx = form.value.tagIds.indexOf(tagId)
  if (idx === -1) {
    form.value.tagIds.push(tagId)
  } else {
    form.value.tagIds.splice(idx, 1)
  }
}

onMounted(() => {
  loadTags()
  loadPost()
})
</script>

<template>
  <div class="mx-auto max-w-3xl">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">
      {{ isEdit ? 'Editar Post' : 'Novo Post' }}
    </h1>

    <LoadingSpinner v-if="loading" />

    <div v-else class="rounded-lg border border-gray-200 bg-white p-6">
      <div v-if="errorMsg"
        class="mb-4 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
        {{ errorMsg }}
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label for="title" class="block text-sm font-medium text-gray-700">Título</label>
          <input id="title" v-model="form.title" type="text" required maxlength="500"
            class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Tags</label>
          <div class="flex flex-wrap gap-2">
            <button v-for="tag in availableTags" :key="tag.id" type="button" @click="toggleTag(tag.id)"
              class="rounded-full px-3 py-1 text-xs font-medium transition-colors"
              :class="form.tagIds.includes(tag.id)
                ? 'bg-sky-100 text-sky-700 border border-sky-300'
                : 'bg-gray-100 text-gray-600 border border-gray-200 hover:bg-gray-200'">
              {{ tag.name }}
            </button>
          </div>
        </div>

        <div>
          <label for="summary" class="block text-sm font-medium text-gray-700">Resumo</label>
          <textarea id="summary" v-model="form.summary" maxlength="1000" rows="3"
            class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Conteúdo</label>
          <EditorBlock
            ref="editorRef"
            v-model="form.html"
            :post-id="postId" />
        </div>

        <ImageUploader v-if="isEdit && postId" :post-id="postId" />

        <div class="flex gap-3 pt-2">
          <button type="submit" :disabled="saving"
            class="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-50">
            {{ saving ? 'Salvando...' : 'Salvar' }}
          </button>
          <button type="button" @click="router.push({ name: 'posts' })"
            class="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">
            Cancelar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
