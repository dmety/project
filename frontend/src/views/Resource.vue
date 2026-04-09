<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">多模态学习资源生成</h1>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800">生成配置</h2>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">知识点ID</label>
                <input v-model.number="generateConfig.knowledgeId" type="number" 
                       class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">资源类型</label>
                <select v-model="generateConfig.resourceType" 
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option value="course_doc">课程讲解文档</option>
                  <option value="mind_map">知识点思维导图</option>
                  <option value="exercise">分难度练习题</option>
                  <option value="code_case">Python代码实操案例</option>
                  <option value="extension_reading">拓展阅读材料</option>
                  <option value="multimodal_diagram">多模态教学图解</option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">难度等级</label>
                <select v-model="generateConfig.difficulty" 
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option value="easy">简单</option>
                  <option value="medium">中等</option>
                  <option value="hard">困难</option>
                </select>
              </div>
              
              <button @click="generateResource" 
                      :disabled="isGenerating"
                      class="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed">
                {{ isGenerating ? '生成中...' : '生成资源' }}
              </button>
            </div>
          </div>
        </div>
        
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow-md p-6">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-xl font-semibold text-gray-800">资源列表</h2>
              <div class="flex space-x-2">
                <select v-model="filterConfig.resourceType" 
                        class="px-3 py-1 border border-gray-300 rounded text-sm focus:outline-none">
                  <option value="">全部类型</option>
                  <option value="course_doc">课程讲解</option>
                  <option value="mind_map">思维导图</option>
                  <option value="exercise">练习题</option>
                  <option value="code_case">代码案例</option>
                  <option value="extension_reading">拓展阅读</option>
                  <option value="multimodal_diagram">教学图解</option>
                </select>
              </div>
            </div>
            
            <div v-if="isGenerating" class="mb-4 p-4 bg-blue-50 rounded-lg">
              <div class="flex items-center space-x-3">
                <div class="w-4 h-4 bg-blue-500 rounded-full animate-pulse"></div>
                <span class="text-blue-700">正在生成资源，请稍候...</span>
              </div>
              <div class="mt-2 bg-blue-200 rounded-full h-2">
                <div class="bg-blue-500 h-2 rounded-full transition-all duration-300" 
                     :style="{ width: generateProgress + '%' }"></div>
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="resource in resources" :key="resource.resourceId" 
                   class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div class="flex justify-between items-start mb-2">
                  <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-medium">
                    {{ getResourceTypeName(resource.resourceType) }}
                  </span>
                  <span class="text-xs text-gray-500">
                    {{ formatDate(resource.generatedAt) }}
                  </span>
                </div>
                <h3 class="font-medium text-gray-800 mb-2">知识点 {{ resource.knowledgeId }}</h3>
                <p class="text-sm text-gray-600 mb-3 line-clamp-2">
                  {{ (resource.resourceContent || '').substring(0, 100) }}...
                </p>
                <div class="flex space-x-2">
                  <button class="text-sm text-blue-500 hover:text-blue-700">查看</button>
                  <button class="text-sm text-green-500 hover:text-green-700">下载</button>
                  <button class="text-sm text-yellow-500 hover:text-yellow-700">收藏</button>
                </div>
              </div>
            </div>
            
            <div v-if="resources.length === 0 && !isGenerating" 
                 class="text-center py-12 text-gray-500">
              <p>暂无资源，点击左侧生成新资源</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { resourceApi } from '@/services/api'
import type { ResourceResponse } from '@/types'

const router = useRouter()
const userStore = useUserStore()

const generateConfig = ref({
  knowledgeId: 1,
  resourceType: 'course_doc',
  difficulty: 'medium'
})

const filterConfig = ref({
  resourceType: ''
})

const resources = ref<ResourceResponse[]>([])
const isGenerating = ref(false)
const generateProgress = ref(0)

const getResourceTypeName = (type: string) => {
  const typeMap: Record<string, string> = {
    course_doc: '课程讲解',
    mind_map: '思维导图',
    exercise: '练习题',
    code_case: '代码案例',
    extension_reading: '拓展阅读',
    multimodal_diagram: '教学图解'
  }
  return typeMap[type] || type
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const generateResource = async () => {
  if (!userStore.userId) return
  
  isGenerating.value = true
  generateProgress.value = 0
  
  try {
    const progressInterval = setInterval(() => {
      generateProgress.value = Math.min(generateProgress.value + 10, 90)
    }, 500)
    
    const res = await resourceApi.generate({
      userId: userStore.userId,
      knowledgeId: generateConfig.value.knowledgeId,
      resourceType: generateConfig.value.resourceType,
      difficulty: generateConfig.value.difficulty
    })
    
    clearInterval(progressInterval)
    generateProgress.value = 100
    
    const data = res.data as any
    resources.value.unshift(data)
    
    setTimeout(() => {
      isGenerating.value = false
      generateProgress.value = 0
    }, 500)
  } catch (error) {
    console.error('生成资源失败:', error)
    isGenerating.value = false
    generateProgress.value = 0
  }
}

const loadResources = async () => {
  if (!userStore.userId) return
  
  try {
    const res = await resourceApi.list({
      userId: userStore.userId,
      resourceType: filterConfig.value.resourceType || undefined
    })
    const data = res.data as any
    resources.value = data.resources || []
  } catch (error) {
    console.error('加载资源列表失败:', error)
  }
}

onMounted(() => {
  if (!userStore.token) {
    router.push('/login')
    return
  }
  loadResources()
})
</script>
