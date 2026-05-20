<script setup lang="ts">
defineProps<{
  message?: string
}>()
</script>

<template>
  <div class="flex flex-col items-center justify-center py-12">
    <div class="size-8 animate-spin rounded-full border-4 border-sky-200 border-t-sky-600" />
    <p v-if="message" class="mt-3 text-sm text-gray-500">{{ message }}</p>
  </div>
</template>
