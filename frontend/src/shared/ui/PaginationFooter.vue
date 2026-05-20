<script setup lang="ts">
const props = defineProps<{
  page: number
  total: number
  pageSize?: number
  label?: string
}>()

const emit = defineEmits<{
  'update:page': [value: number]
}>()

const pageSize = props.pageSize || 20

function prev() {
  emit('update:page', props.page - 1)
}

function next() {
  emit('update:page', props.page + 1)
}
</script>

<template>
  <div
    v-if="total > pageSize"
    class="flex items-center justify-between border-t border-gray-200 px-6 py-3"
  >
    <span class="text-sm text-gray-600">
      {{ total }} {{ label || 'item(ns)' }}
    </span>
    <div class="flex gap-2">
      <button
        :disabled="page <= 1"
        @click="prev"
        class="rounded-md border border-gray-300 px-3 py-1 text-sm disabled:opacity-50"
      >
        Anterior
      </button>
      <button
        :disabled="page * pageSize >= total"
        @click="next"
        class="rounded-md border border-gray-300 px-3 py-1 text-sm disabled:opacity-50"
      >
        Próximo
      </button>
    </div>
  </div>
</template>
