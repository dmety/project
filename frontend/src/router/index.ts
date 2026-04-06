import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue')
  },
  {
    path: '/resource',
    name: 'Resource',
    component: () => import('@/views/Resource.vue')
  },
  {
    path: '/path',
    name: 'Path',
    component: () => import('@/views/Path.vue')
  },
  {
    path: '/tutor',
    name: 'Tutor',
    component: () => import('@/views/Tutor.vue')
  },
  {
    path: '/evaluation',
    name: 'Evaluation',
    component: () => import('@/views/Evaluation.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
