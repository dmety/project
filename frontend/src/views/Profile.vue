<template>
  <div class="flex h-screen bg-gray-50">
    <div class="w-1/2 p-6 overflow-y-auto">
      <div class="bg-white rounded-lg shadow-md p-6 h-full">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">学生画像看板</h2>
        
        <div class="grid grid-cols-1 gap-6">
          <div class="bg-gray-50 rounded-lg p-4">
            <h3 class="text-lg font-semibold mb-4 text-gray-700">7维度能力雷达图</h3>
            <div class="h-80">
              <v-chart :option="radarOption" autoresize />
            </div>
          </div>
          
          <div class="bg-gray-50 rounded-lg p-4">
            <h3 class="text-lg font-semibold mb-4 text-gray-700">学习状态热力图</h3>
            <div class="h-64">
              <v-chart :option="heatmapOption" autoresize />
            </div>
          </div>
          
          <div class="bg-gray-50 rounded-lg p-4">
            <h3 class="text-lg font-semibold mb-4 text-gray-700">画像详情</h3>
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-600">知识基础水平:</span>
                <span class="font-medium">{{ profileData?.dimensionDetails?.knowledgeLevel || '-' }}/10</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">认知风格:</span>
                <span class="font-medium">{{ profileData?.dimensionDetails?.cognitiveStyle || '-' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">学习节奏:</span>
                <span class="font-medium">{{ profileData?.dimensionDetails?.learningPace || '-' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">学习目标:</span>
                <span class="font-medium">{{ profileData?.dimensionDetails?.learningGoals || '-' }}</span>
              </div>
              <div>
                <span class="text-gray-600">知识薄弱点:</span>
                <div class="mt-1 flex flex-wrap gap-2">
                  <span v-for="(item, index) in profileData?.dimensionDetails?.knowledgeWeakness" :key="index" 
                        class="px-2 py-1 bg-red-100 text-red-700 rounded text-sm">
                    {{ item }}
                  </span>
                </div>
              </div>
              <div>
                <span class="text-gray-600">兴趣方向:</span>
                <div class="mt-1 flex flex-wrap gap-2">
                  <span v-for="(item, index) in profileData?.dimensionDetails?.interestDirections" :key="index" 
                        class="px-2 py-1 bg-blue-100 text-blue-700 rounded text-sm">
                    {{ item }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="w-1/2 flex flex-col border-l border-gray-200">
      <div class="bg-white p-4 border-b border-gray-200">
        <h2 class="text-xl font-bold text-gray-800">AI 画像构建助手</h2>
        <p class="text-sm text-gray-500">通过自然对话完成画像初始化</p>
      </div>
      
      <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="chatContainer">
        <div v-for="(msg, index) in messages" :key="index" 
             :class="['flex', msg.role === 'user' ? 'justify-end' : 'justify-start']">
          <div :class="['max-w-[80%] rounded-lg p-3', 
                       msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-white border border-gray-200']">
            <div v-if="msg.role === 'assistant'" class="prose prose-sm max-w-none">
              <div v-html="renderMarkdown(msg.content)"></div>
            </div>
            <div v-else>{{ msg.content }}</div>
          </div>
        </div>
        
        <div v-if="isLoading" class="flex justify-start">
          <div class="bg-white border border-gray-200 rounded-lg p-3">
            <div class="flex space-x-2">
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="bg-white p-4 border-t border-gray-200">
        <div class="flex space-x-2">
          <textarea v-model="inputMessage" 
                    @keydown.enter.prevent="sendMessage"
                    class="flex-1 border border-gray-300 rounded-lg px-4 py-2 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="输入消息，开始构建您的学习画像..."
                    rows="2"></textarea>
          <button @click="sendMessage" 
                  :disabled="!inputMessage.trim() || isLoading"
                  class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed">
            发送
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { RadarChart, HeatmapChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  VisualMapComponent
} from 'echarts/components'
import type { EChartsOption } from 'echarts'
import { marked } from 'marked'
import { profileApi } from '@/services/api'
import type { ProfileVisualizationData, ChatMessage } from '@/types'

use([
  CanvasRenderer,
  RadarChart,
  HeatmapChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  VisualMapComponent
])

const router = useRouter()
const userStore = useUserStore()
const chatContainer = ref<HTMLElement>()

const messages = ref<ChatMessage[]>([
  {
    role: 'assistant',
    content: '您好！我是您的学习画像构建助手。请告诉我一些关于您的学习情况，比如：\n\n- 您目前的Python基础如何？\n- 您喜欢什么样的学习方式？\n- 您的学习目标是什么？\n\n通过我们的对话，我会帮您构建一个完整的学习画像！'
  }
])
const inputMessage = ref('')
const isLoading = ref(false)
const conversationId = ref<string>()
const profileData = ref<ProfileVisualizationData>()

const radarOption = computed<EChartsOption>(() => {
  const radarData = profileData.value?.radarData || {
    '知识基础': 5,
    '学习风格': 7,
    '学习目标': 6,
    '学习节奏': 6.5,
    '兴趣方向': 7.5,
    '学习习惯': 6,
    '实践能力': 5.5
  }
  
  return {
    tooltip: {},
    radar: {
      indicator: Object.keys(radarData).map(key => ({
        name: key,
        max: 10
      }))
    },
    series: [{
      type: 'radar',
      data: [{
        value: Object.values(radarData),
        name: '能力画像',
        areaStyle: {
          color: 'rgba(59, 130, 246, 0.3)'
        },
        lineStyle: {
          color: '#3b82f6'
        },
        itemStyle: {
          color: '#3b82f6'
        }
      }]
    }]
  }
})

const heatmapOption = computed<EChartsOption>(() => {
  const heatmapData = profileData.value?.heatmapData || [
    [5, 6.5, 5.5, 7],
    [6, 7, 6, 6.5],
    [5.5, 6, 7.5, 5.5],
    [7, 6.5, 5.5, 6]
  ]
  
  const hours = ['周一', '周二', '周三', '周四']
  const days = ['上午', '下午', '晚上', '深夜']
  
  const data = []
  for (let i = 0; i < hours.length; i++) {
    for (let j = 0; j < days.length; j++) {
      data.push([j, i, heatmapData[i][j]])
    }
  }
  
  return {
    tooltip: {
      position: 'top'
    },
    grid: {
      height: '50%',
      top: '10%'
    },
    xAxis: {
      type: 'category',
      data: days,
      splitArea: {
        show: true
      }
    },
    yAxis: {
      type: 'category',
      data: hours,
      splitArea: {
        show: true
      }
    },
    visualMap: {
      min: 0,
      max: 10,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '5%',
      inRange: {
        color: ['#e0f3f8', '#abd9e9', '#74add1', '#4575b4', '#313695']
      }
    },
    series: [{
      name: '学习状态',
      type: 'heatmap',
      data: data,
      label: {
        show: true
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
})

const renderMarkdown = (content: string) => {
  return marked(content)
}

const loadProfileData = async () => {
  if (!userStore.userId) return
  
  try {
    const res = await profileApi.getVisualization(userStore.userId)
    profileData.value = res.data as any
  } catch (error) {
    console.error('加载画像数据失败:', error)
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isLoading.value || !userStore.userId) return
  
  const message = inputMessage.value
  messages.value.push({
    role: 'user',
    content: message
  })
  inputMessage.value = ''
  isLoading.value = true
  
  await nextTick()
  scrollToBottom()
  
  try {
    const res = await profileApi.dialog({
      userId: userStore.userId,
      message: message,
      conversationId: conversationId.value
    })
    
    const data = res.data as any
    conversationId.value = data.conversationId
    messages.value.push({
      role: 'assistant',
      content: data.assistantMessage
    })
    
    await loadProfileData()
  } catch (error) {
    console.error('发送消息失败:', error)
    messages.value.push({
      role: 'assistant',
      content: '抱歉，发生了一些错误，请稍后重试。'
    })
  } finally {
    isLoading.value = false
    await nextTick()
    scrollToBottom()
  }
}

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

onMounted(() => {
  if (!userStore.token) {
    router.push('/login')
    return
  }
  loadProfileData()
})
</script>

<style scoped>
.prose :where(code):not(:where([class~="not-prose"] *)) {
  background-color: rgba(107, 114, 128, 0.1);
  border-radius: 0.25rem;
  padding: 0.125rem 0.25rem;
  font-size: 0.875em;
}
</style>
