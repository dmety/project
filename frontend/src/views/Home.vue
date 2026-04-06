<template>
  <div class="home min-h-screen bg-gray-50">
    <nav class="bg-white shadow-md">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-bold text-gray-800">个性化学习系统</h1>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/profile" 
                         class="px-3 py-2 text-gray-600 hover:text-blue-500 hover:bg-blue-50 rounded-lg transition-colors">
              学生画像
            </router-link>
            <router-link to="/resource" 
                         class="px-3 py-2 text-gray-600 hover:text-blue-500 hover:bg-blue-50 rounded-lg transition-colors">
              学习资源
            </router-link>
            <router-link to="/path" 
                         class="px-3 py-2 text-gray-600 hover:text-blue-500 hover:bg-blue-50 rounded-lg transition-colors">
              学习路径
            </router-link>
            <router-link to="/tutor" 
                         class="px-3 py-2 text-gray-600 hover:text-blue-500 hover:bg-blue-50 rounded-lg transition-colors">
              智能辅导
            </router-link>
            <router-link to="/evaluation" 
                         class="px-3 py-2 text-gray-600 hover:text-blue-500 hover:bg-blue-50 rounded-lg transition-colors">
              学习评估
            </router-link>
            <button v-if="userStore.token" 
                    @click="logout"
                    class="px-3 py-2 text-red-500 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors">
              退出登录
            </button>
            <router-link v-else to="/login" 
                         class="px-3 py-2 text-blue-500 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors">
              登录
            </router-link>
          </div>
        </div>
      </div>
    </nav>
    
    <div class="max-w-7xl mx-auto px-4 py-12">
      <div class="text-center mb-12">
        <h2 class="text-4xl font-bold text-gray-800 mb-4">欢迎使用个性化学习系统</h2>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          基于大模型的个性化资源生成与学习多智能体系统，为您提供智能、个性化的学习体验
        </p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link to="/profile" 
                     class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <span class="text-2xl">🎯</span>
          </div>
          <h3 class="text-xl font-semibold text-gray-800 mb-2">对话式动态学生画像</h3>
          <p class="text-gray-600">通过自然对话完成画像初始化，7维度可视化展示</p>
        </router-link>
        
        <router-link to="/resource" 
                     class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
            <span class="text-2xl">📚</span>
          </div>
          <h3 class="text-xl font-semibold text-gray-800 mb-2">多模态学习资源生成</h3>
          <p class="text-gray-600">6种资源类型，智能生成，实时进度展示</p>
        </router-link>
        
        <router-link to="/path" 
                     class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
            <span class="text-2xl">🗺️</span>
          </div>
          <h3 class="text-xl font-semibold text-gray-800 mb-2">个性化学习路径规划</h3>
          <p class="text-gray-600">基于知识点依赖关系，动态调整学习路径</p>
        </router-link>
        
        <router-link to="/tutor" 
                     class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-4">
            <span class="text-2xl">🤖</span>
          </div>
          <h3 class="text-xl font-semibold text-gray-800 mb-2">多模态智能辅导</h3>
          <p class="text-gray-600">文字、图片、代码多种提问方式，在线代码运行</p>
        </router-link>
        
        <router-link to="/evaluation" 
                     class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-4">
            <span class="text-2xl">📊</span>
          </div>
          <h3 class="text-xl font-semibold text-gray-800 mb-2">学习效果评估</h3>
          <p class="text-gray-600">多维度量化评估，知识漏洞定位</p>
        </router-link>
        
        <div class="bg-white rounded-xl shadow-md p-6">
          <div class="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
            <span class="text-2xl">🛡️</span>
          </div>
          <h3 class="text-xl font-semibold text-gray-800 mb-2">防幻觉与内容安全</h3>
          <p class="text-gray-600">全链路内容安全管控，讯飞API对接</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()

const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>
