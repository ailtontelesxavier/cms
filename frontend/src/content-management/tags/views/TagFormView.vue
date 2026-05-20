<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { tagsApi } from '@/shared/api/tags'
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
  slug: '',
  description: '',
})

async function loadTag() {
  if (!route.params.id) return
  loading.value = true
  try {
    const res = await tagsApi.getById(Number(route.params.id))
    const tag = res.data
    form.value = { name: tag.name, slug: tag.slug, description: tag.description || '' }
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
      await tagsApi.update(Number(route.params.id), {
        name: form.value.name,
        description: form.value.description || null,
      })
    } else {
      await tagsApi.create({
        name: form.value.name,
        slug: form.value.slug,
        description: form.value.description || null,
      })
    }
    router.push({ name: 'tags' })
  } catch (err) {
    errorMsg.value = getApiErrorMessage(err)
  } finally {
    saving.value = false
  }
}

onMounted(loadTag)
</script>

<template>
  <div class="mx-auto max-w-lg">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">
      {{ isEdit ? 'Editar Tag' : 'Nova Tag' }}
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
          <label for="slug" class="block text-sm font-medium text-gray-700">Slug</label>
          <input id="slug" v-model="form.slug" type="text" required maxlength="100" :disabled="isEdit"
            class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500 disabled:bg-gray-100 disabled:text-gray-500" />
        </div>

        <div>
          <label for="description" class="block text-sm font-medium text-gray-700">Descrição</label>
          <textarea id="description" v-model="form.description" maxlength="500" rows="3"
            class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" />
        </div>

        <div class="flex gap-3 pt-2">
          <button type="submit" :disabled="saving"
            class="rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-50">
            {{ saving ? 'Salvando...' : 'Salvar' }}
          </button>
          <button type="button" @click="router.push({ name: 'tags' })"
            class="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">
            Cancelar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
