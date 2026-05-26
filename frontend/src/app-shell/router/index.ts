import { createRouter, createWebHistory } from 'vue-router'
import { authGuard } from '@/app-shell/guards/auth.guard'
import { mfaGuard } from '@/app-shell/guards/mfa.guard'
import { permissionGuard } from '@/app-shell/guards/permission.guard'

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    requiresMfa?: boolean
    module?: string
    action?: string
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
          meta: { module: 'tags', action: 'criar' },
        },
        {
          path: 'tags/:id/edit',
          name: 'tag-edit',
          component: () => import('@/content-management/tags/views/TagFormView.vue'),
          props: true,
          meta: { module: 'tags', action: 'atualizar' },
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
          meta: { module: 'posts', action: 'criar' },
        },
        {
          path: 'posts/:id/edit',
          name: 'post-edit',
          component: () => import('@/content-management/posts/views/PostFormView.vue'),
          props: true,
          meta: { module: 'posts', action: 'atualizar' },
        },
        {
          path: 'roles',
          name: 'roles',
          component: () => import('@/role-management/views/RoleListView.vue'),
        },
        {
          path: 'roles/new',
          name: 'role-create',
          component: () => import('@/role-management/views/RoleFormView.vue'),
          meta: { module: 'administrativo', action: 'criar' },
        },
        {
          path: 'roles/:id/edit',
          name: 'role-edit',
          component: () => import('@/role-management/views/RoleEditView.vue'),
          props: true,
          meta: { module: 'administrativo', action: 'atualizar' },
        },
        {
          path: 'users',
          name: 'users',
          component: () => import('@/user-management/views/UserListView.vue'),
          meta: { module: 'auth', action: 'ler' },
        },
        {
          path: 'users/new',
          name: 'user-create',
          component: () => import('@/user-management/views/UserFormView.vue'),
          meta: { module: 'auth', action: 'criar' },
        },
        {
          path: 'users/:id/edit',
          name: 'user-edit',
          component: () => import('@/user-management/views/UserFormView.vue'),
          props: true,
          meta: { module: 'auth', action: 'atualizar' },
        },
      ],
    },
  ],
})

router.beforeEach(authGuard)
router.beforeEach(mfaGuard)
router.beforeEach(permissionGuard)

export default router
