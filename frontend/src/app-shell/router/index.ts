import { createRouter, createWebHistory } from 'vue-router'
import { useSessionStore } from '@/auth-session/stores/session'

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
  }
}

const router = createRouter({
  history: createWebHistory('/admin'),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/auth-session/views/LoginView.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/mfa-required',
      name: 'mfa-required',
      component: () => import('@/auth-session/views/MfaRequiredView.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/',
      component: () => import('@/app-shell/components/AppLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          redirect: { name: 'posts' },
        },
        {
          path: 'mfa/setup',
          name: 'mfa-setup',
          component: () => import('@/auth-session/views/MfaSetupView.vue'),
        },
        {
          path: 'mfa/verify',
          name: 'mfa-verify',
          component: () => import('@/auth-session/views/MfaVerifyView.vue'),
        },
        {
          path: 'tags',
          name: 'tags',
          component: () => import('@/content-management/tags/views/TagListView.vue'),
        },
        {
          path: 'tags/new',
          name: 'tag-create',
          component: () => import('@/content-management/tags/views/TagFormView.vue'),
        },
        {
          path: 'tags/:id/edit',
          name: 'tag-edit',
          component: () => import('@/content-management/tags/views/TagFormView.vue'),
          props: true,
        },
        {
          path: 'posts',
          name: 'posts',
          component: () => import('@/content-management/posts/views/PostListView.vue'),
        },
        {
          path: 'posts/new',
          name: 'post-create',
          component: () => import('@/content-management/posts/views/PostFormView.vue'),
        },
        {
          path: 'posts/:id/edit',
          name: 'post-edit',
          component: () => import('@/content-management/posts/views/PostFormView.vue'),
          props: true,
        },
      ],
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const session = useSessionStore()

  if (to.meta.requiresAuth && !session.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.name === 'login' && session.isAuthenticated) {
    next({ name: 'posts' })
  } else {
    next()
  }
})

export default router
