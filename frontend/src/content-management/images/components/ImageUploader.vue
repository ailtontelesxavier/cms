<script setup lang="ts">
import { ref } from 'vue'
import { postsApi } from '@/shared/api/posts'
import { getApiErrorMessage } from '@/shared/api/client'
import type { ImageUploadResult } from '@/shared/types/posts'

const props = defineProps<{
  postId: string
}>()

const images = ref<ImageUploadResult[]>([])
const uploading = ref(false)
const errorMsg = ref('')

async function handleUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  uploading.value = true
  errorMsg.value = ''

  try {
    const res = await postsApi.uploadImage(props.postId, file)
    images.value.push(res.data)
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    uploading.value = false
    input.value = ''
  }
}

async function handleDelete(imageId: string) {
  try {
    await postsApi.deleteImage(props.postId, imageId)
    images.value = images.value.filter(img => img.image_id !== imageId)
  } catch (err) {
    alert(getApiErrorMessage(err))
  }
}
</script>

<template>
  <div class="rounded-lg border border-gray-200 p-4">
    <h3 class="text-sm font-medium text-gray-700 mb-3">Imagens do Post</h3>

    <div v-if="errorMsg"
      class="mb-3 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <div class="flex flex-wrap gap-3 mb-3">
      <div v-for="img in images" :key="img.image_id"
        class="relative group rounded-md border border-gray-200 overflow-hidden">
        <img :src="img.url" alt="" class="size-24 object-cover" />
        <button @click="handleDelete(img.image_id)"
          class="absolute top-1 right-1 rounded-full bg-red-600 text-white p-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <svg class="size-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <label
      class="inline-flex cursor-pointer items-center gap-2 rounded-md border border-dashed border-gray-300 px-4 py-2 text-sm text-gray-600 hover:border-gray-400 hover:text-gray-700">
      <svg class="size-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      {{ uploading ? 'Enviando...' : 'Upload de imagem' }}
      <input type="file" accept="image/jpeg,image/png,image/webp" class="hidden" @change="handleUpload" :disabled="uploading" />
    </label>
  </div>
</template>
