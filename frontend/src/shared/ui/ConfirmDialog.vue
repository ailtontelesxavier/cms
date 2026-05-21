<script setup lang="ts">
defineProps<{
  open: boolean
  title?: string
  message?: string
  confirmLabel?: string
  confirmClass?: string
  loading?: boolean
}>()

const emit = defineEmits<{
  confirm: []
  cancel: []
}>()
</script>

<template>
  <Teleport to="body">
    <div
      v-if="open"
      class="fixed inset-0 z-50 flex items-center justify-center"
    >
      <div class="fixed inset-0 bg-black/50" @click="emit('cancel')" />
      <div class="relative z-10 w-full max-w-sm rounded-lg bg-white p-6 shadow-xl">
        <h3 class="text-lg font-semibold text-gray-900 mb-2">
          {{ title || 'Confirmação' }}
        </h3>
        <p class="text-sm text-gray-600 mb-6">
          {{ message || 'Tem certeza que deseja continuar?' }}
        </p>
        <div class="flex justify-end gap-3">
          <button
            @click="emit('cancel')"
            :disabled="loading"
            class="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
          >
            Cancelar
          </button>
          <button
            @click="emit('confirm')"
            :disabled="loading"
            :class="confirmClass || 'rounded-md bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500 disabled:opacity-50'"
          >
            {{ loading ? 'Aguarde...' : (confirmLabel || 'Confirmar') }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
