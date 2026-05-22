<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useSessionStore } from '@/auth-session/stores/session'

const session = useSessionStore()
const router = useRouter()
const sidebarOpen = ref(false)

function handleLogout() {
  session.clearSession()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="flex h-screen bg-gray-50">
    <aside
      class="fixed inset-y-0 left-0 z-30 w-64 transform bg-white shadow-lg transition-transform duration-200 lg:static lg:translate-x-0"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="flex h-16 items-center border-b border-gray-200 px-6">
        <h1 class="text-lg font-bold text-gray-900">CMS Admin</h1>
      </div>

      <nav class="mt-4 space-y-1 px-3">
        <router-link
          v-for="item in [
            { name: 'posts', label: 'Posts', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
            { name: 'tags', label: 'Tags', icon: 'M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z' },
            { name: 'roles', label: 'Perfis', icon: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' },
            { name: 'users', label: 'Usuários', icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z' },
          ]"
          :key="item.name"
          :to="{ name: item.name }"
          class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900"
          active-class="bg-sky-50 text-sky-700"
        >
          <svg class="size-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
          </svg>
          {{ item.label }}
        </router-link>
      </nav>

      <div class="absolute bottom-0 left-0 right-0 border-t border-gray-200 p-4">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-600 truncate">{{ session.currentUser?.name }}</div>
          <button @click="handleLogout" class="text-sm text-red-600 hover:text-red-500">
            Sair
          </button>
        </div>
      </div>
    </aside>

    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-20 bg-black/30 lg:hidden"
      @click="sidebarOpen = false"
    />

    <div class="flex flex-1 flex-col min-w-0">
      <header class="flex h-16 items-center gap-4 border-b border-gray-200 bg-white px-6 lg:hidden">
        <button @click="sidebarOpen = true" class="text-gray-500 hover:text-gray-700">
          <svg class="size-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <h1 class="text-lg font-bold text-gray-900">CMS Admin</h1>
      </header>

      <main class="flex-1 overflow-y-auto p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>
