<script setup lang="ts">
defineProps<{
  message?: string
}>()

defineEmits<{
  retry: []
}>()
</script>

<template>
  <div class="rounded-lg border border-red-200 bg-red-50 p-4">
    <div class="flex items-start gap-3">
      <svg class="mt-0.5 size-5 shrink-0 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <div class="flex-1">
        <p class="text-sm text-red-700">{{ message || 'Ocorreu um erro ao carregar os dados' }}</p>
        <button @click="$emit('retry')"
          class="mt-2 text-sm font-medium text-red-600 hover:text-red-500">
          Tentar novamente
        </button>
      </div>
    </div>
  </div>
</template>
