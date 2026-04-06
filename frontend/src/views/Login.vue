<template>
  <div class="login min-h-screen flex items-center justify-center bg-gray-50">
    <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
      <h2 class="text-2xl font-bold text-center mb-6">用户登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
            用户名
          </label>
          <input
            id="username"
            type="text"
            v-model="form.username"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="请输入用户名"
          />
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
            密码
          </label>
          <input
            id="password"
            type="password"
            v-model="form.password"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="请输入密码"
          />
        </div>
        <div v-if="error" class="mb-4 text-red-500 text-sm">
          {{ error }}
        </div>
        <div class="flex items-center justify-between">
          <button
            type="submit"
            :disabled="loading"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50"
          >
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { authApi } from '@/services/api'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({
  username: '',
  password: ''
})
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const res = await authApi.login(form) as any
    if (res.code === 200) {
      userStore.setAuthData(res.data)
      router.push('/')
    } else {
      error.value = res.message || '登录失败'
    }
  } catch (err: any) {
    error.value = err.message || '登录失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>
