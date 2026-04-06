import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/store/user'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { requiresAuth: true, permission: 'profile:query' }
  },
  {
    path: '/resource',
    name: 'Resource',
    component: () => import('@/views/Resource.vue'),
    meta: { requiresAuth: true, permission: 'resource:query' }
  },
  {
    path: '/path',
    name: 'Path',
    component: () => import('@/views/Path.vue'),
    meta: { requiresAuth: true, permission: 'path:query' }
  },
  {
    path: '/tutor',
    name: 'Tutor',
    component: () => import('@/views/Tutor.vue'),
    meta: { requiresAuth: true, permission: 'tutor:chat' }
  },
  {
    path: '/evaluation',
    name: 'Evaluation',
    component: () => import('@/views/Evaluation.vue'),
    meta: { requiresAuth: true, permission: 'evaluation:query' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth !== false) {
    if (!userStore.token) {
      next('/login')
      return
    }
    
    if (to.meta.permission) {
      const permission = to.meta.permission as string
      if (!userStore.hasPermission(permission)) {
        alert('无权限访问该页面')
        next('/')
        return
      }
    }
  }
  
  if (to.path === '/login' && userStore.token) {
    next('/')
    return
  }
  
  next()
})

export default router
