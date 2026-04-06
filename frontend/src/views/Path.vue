<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-7xl mx-auto">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-gray-800">个性化学习路径规划</h1>
        <button @click="showGenerateModal = true" 
                class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
          生成新路径
        </button>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800">学习路径</h2>
            
            <div v-if="selectedPath" class="mb-6">
              <div class="flex justify-between items-center mb-4">
                <div>
                  <h3 class="text-lg font-medium text-gray-800">{{ selectedPath.pathName }}</h3>
                  <p class="text-sm text-gray-500">
                    进度: {{ selectedPath.currentProgress.toFixed(1) }}% | 
                    里程碑: {{ selectedPath.completedMilestones }}/{{ selectedPath.totalMilestones }}
                  </p>
                </div>
                <div class="w-32 bg-gray-200 rounded-full h-2">
                  <div class="bg-blue-500 h-2 rounded-full" 
                       :style="{ width: selectedPath.currentProgress + '%' }"></div>
                </div>
              </div>
              
              <div class="relative">
                <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200"></div>
                
                <div v-for="(node, index) in selectedPath.nodes" :key="node.nodeId" 
                     class="relative pl-12 pb-8 last:pb-0">
                  <div class="absolute left-0 w-8 h-8 rounded-full flex items-center justify-center border-2"
                       :class="node.completionStatus === 1 
                                ? 'bg-green-500 border-green-500 text-white' 
                                : node.milestoneFlag 
                                  ? 'bg-yellow-100 border-yellow-500 text-yellow-700' 
                                  : 'bg-white border-gray-300 text-gray-600'">
                    {{ node.completionStatus === 1 ? '✓' : index + 1 }}
                  </div>
                  
                  <div class="bg-gray-50 rounded-lg p-4">
                    <div class="flex justify-between items-start mb-2">
                      <div>
                        <h4 class="font-medium text-gray-800">
                          {{ node.milestoneFlag ? '🏆 ' : '' }}知识点 {{ node.knowledgeId }}
                        </h4>
                        <p class="text-sm text-gray-600">{{ node.learningContent }}</p>
                      </div>
                      <div class="text-right">
                        <span v-if="node.planCompletionTime" class="text-xs text-gray-500">
                          计划: {{ formatDate(node.planCompletionTime) }}
                        </span>
                        <span v-if="node.actualCompletionTime" class="text-xs text-green-600 block">
                          完成: {{ formatDate(node.actualCompletionTime) }}
                        </span>
                      </div>
                    </div>
                    
                    <div class="flex space-x-2 mt-2">
                      <button v-if="node.completionStatus === 0" 
                              @click="markComplete(node)"
                              class="text-sm text-green-500 hover:text-green-700">
                        标记完成
                      </button>
                      <button class="text-sm text-blue-500 hover:text-blue-700">查看资源</button>
                      <button class="text-sm text-purple-500 hover:text-purple-700">开始学习</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else class="text-center py-12 text-gray-500">
              <p>请选择或生成一个学习路径</p>
            </div>
          </div>
        </div>
        
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800">我的路径</h2>
            <div class="space-y-3">
              <div v-for="path in paths" :key="path.pathId"
                   @click="selectedPath = path"
                   :class="['p-3 rounded-lg cursor-pointer transition-colors',
                            selectedPath?.pathId === path.pathId 
                              ? 'bg-blue-50 border-2 border-blue-500' 
                              : 'bg-gray-50 hover:bg-gray-100 border-2 border-transparent']">
                <div class="flex justify-between items-center">
                  <h3 class="font-medium text-gray-800">{{ path.pathName }}</h3>
                  <span class="text-sm text-blue-600">{{ path.currentProgress.toFixed(0) }}%</span>
                </div>
                <p class="text-xs text-gray-500 mt-1">
                  {{ formatDate(path.createdAt) }}
                </p>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800">资源推送</h2>
            <div class="space-y-3">
              <div v-for="item in pushedResources" :key="item.resourceId"
                   class="p-3 bg-gray-50 rounded-lg">
                <div class="flex justify-between items-start">
                  <div>
                    <span class="text-xs px-2 py-0.5 bg-blue-100 text-blue-700 rounded">
                      {{ getResourceTypeName(item.resourceType) }}
                    </span>
                    <h4 class="font-medium text-gray-800 mt-1">知识点 {{ item.knowledgeId }}</h4>
                  </div>
                  <span v-if="item.readStatus === 0" 
                        class="w-2 h-2 bg-red-500 rounded-full"></span>
                </div>
                <button class="text-sm text-blue-500 hover:text-blue-700 mt-2">
                  {{ item.readStatus === 0 ? '标记已读' : '已读' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="showGenerateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-6 w-full max-w-md">
          <h3 class="text-xl font-semibold mb-4">生成学习路径</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">路径名称</label>
              <input v-model="newPathConfig.pathName" type="text" 
                     class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">起始知识点ID</label>
              <input v-model.number="newPathConfig.startKnowledgeId" type="number" 
                     class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
          </div>
          <div class="flex justify-end space-x-3 mt-6">
            <button @click="showGenerateModal = false" 
                    class="px-4 py-2 text-gray-600 hover:text-gray-800">
              取消
            </button>
            <button @click="generatePath" 
                    :disabled="isGenerating"
                    class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50">
              {{ isGenerating ? '生成中...' : '生成' }}
            </button>
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
import { pathApi } from '@/services/api'
import type { LearningPathResponse, ResourcePushItem } from '@/types'

const router = useRouter()
const userStore = useUserStore()

const paths = ref<LearningPathResponse[]>([])
const selectedPath = ref<LearningPathResponse>()
const pushedResources = ref<ResourcePushItem[]>([])
const showGenerateModal = ref(false)
const isGenerating = ref(false)

const newPathConfig = ref({
  pathName: '',
  startKnowledgeId: 1
})

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

const markComplete = async (node: any) => {
  try {
    await pathApi.updateNode({
      nodeId: node.nodeId,
      completionStatus: 1
    })
    node.completionStatus = 1
    node.actualCompletionTime = new Date().toISOString()
    
    if (selectedPath.value) {
      const completed = selectedPath.value.nodes.filter(n => n.completionStatus === 1).length
      selectedPath.value.currentProgress = (completed / selectedPath.value.nodes.length) * 100
    }
  } catch (error) {
    console.error('标记完成失败:', error)
  }
}

const generatePath = async () => {
  if (!userStore.userInfo?.userId || !newPathConfig.value.pathName) return
  
  isGenerating.value = true
  
  try {
    const res = await pathApi.generate({
      userId: userStore.userInfo.userId,
      pathName: newPathConfig.value.pathName,
      startKnowledgeId: newPathConfig.value.startKnowledgeId
    })
    
    paths.value.unshift(res.data)
    selectedPath.value = res.data
    showGenerateModal.value = false
    newPathConfig.value.pathName = ''
  } catch (error) {
    console.error('生成路径失败:', error)
  } finally {
    isGenerating.value = false
  }
}

const loadPaths = async () => {
  if (!userStore.userInfo?.userId) return
  
  try {
    const res = await pathApi.list(userStore.userInfo.userId)
    paths.value = res.data || []
    if (paths.value.length > 0) {
      selectedPath.value = paths.value[0]
    }
  } catch (error) {
    console.error('加载路径列表失败:', error)
  }
}

const loadPushedResources = async () => {
  if (!userStore.userInfo?.userId) return
  
  try {
    const res = await pathApi.push({
      userId: userStore.userInfo.userId
    })
    pushedResources.value = res.data || []
  } catch (error) {
    console.error('加载推送资源失败:', error)
  }
}

onMounted(() => {
  if (!userStore.token) {
    router.push('/login')
    return
  }
  loadPaths()
  loadPushedResources()
})
</script>
