<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-7xl mx-auto">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-gray-800">学习效果评估</h1>
        <button @click="generateEvaluation"
                :disabled="isGenerating"
                class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50">
          {{ isGenerating ? '生成中...' : '生成评估报告' }}
        </button>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-4 text-gray-800">知识点掌握度趋势</h2>
          <div class="h-64">
            <v-chart :option="knowledgeMasteryOption" autoresize />
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-4 text-gray-800">答题正确率趋势</h2>
          <div class="h-64">
            <v-chart :option="answerAccuracyOption" autoresize />
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-4 text-gray-800">学习进度完成率趋势</h2>
          <div class="h-64">
            <v-chart :option="progressCompletionOption" autoresize />
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-4 text-gray-800">能力提升幅度趋势</h2>
          <div class="h-64">
            <v-chart :option="abilityImprovementOption" autoresize />
          </div>
        </div>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-4 text-gray-800">历史评估报告</h2>
          <div class="space-y-4">
            <div v-for="report in recentEvaluations" :key="report.evaluationId"
                 class="border border-gray-200 rounded-lg p-4">
              <div class="flex justify-between items-start mb-2">
                <div>
                  <h3 class="font-medium text-gray-800">评估周期: {{ report.evaluationPeriod }}</h3>
                  <p class="text-sm text-gray-500">{{ formatDate(report.generatedAt) }}</p>
                </div>
                <div class="text-right">
                  <span class="text-lg font-bold text-blue-600">{{ report.knowledgeMastery.toFixed(1) }}/10</span>
                  <p class="text-xs text-gray-500">掌握度</p>
                </div>
              </div>
              <div class="grid grid-cols-3 gap-4 text-sm mb-3">
                <div>
                  <span class="text-gray-500">答题正确率:</span>
                  <span class="font-medium ml-1">{{ report.answerAccuracy.toFixed(1) }}%</span>
                </div>
                <div>
                  <span class="text-gray-500">进度完成率:</span>
                  <span class="font-medium ml-1">{{ report.learningProgressCompletion?.toFixed(1) || 0 }}%</span>
                </div>
                <div>
                  <span class="text-gray-500">能力提升:</span>
                  <span class="font-medium ml-1">{{ report.abilityImprovement.toFixed(1) }}%</span>
                </div>
              </div>
              <div>
                <span class="text-gray-600">知识漏洞:</span>
                <div class="mt-1 flex flex-wrap gap-2">
                  <span v-for="(gap, index) in report.knowledgeGaps" :key="index"
                        class="px-2 py-1 bg-red-100 text-red-700 rounded text-sm">
                    {{ gap }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-4 text-gray-800">知识漏洞定位</h2>
          <div class="space-y-3">
            <div v-for="(gap, index) in knowledgeGaps" :key="index"
                 class="p-3 bg-red-50 rounded-lg">
              <div class="flex justify-between items-center">
                <span class="font-medium text-red-800">{{ gap }}</span>
                <span class="text-sm text-red-600">需加强</span>
              </div>
              <div class="mt-2 flex space-x-2">
                <button class="text-sm text-blue-500 hover:text-blue-700">查看资源</button>
                <button class="text-sm text-green-500 hover:text-green-700">开始练习</button>
              </div>
            </div>
          </div>
          
          <div v-if="knowledgeGaps.length === 0" class="text-center py-8 text-gray-500">
            <p>暂无知识漏洞，继续保持！</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import type { EChartsOption } from 'echarts'
import { evaluationApi } from '@/services/api'

use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

const router = useRouter()
const userStore = useUserStore()

const isGenerating = ref(false)
const recentEvaluations = ref<any[]>([])
const knowledgeGaps = ref<string[]>(['知识点2', '知识点5', '知识点7'])

const generateTrendData = (baseValue: number, label: string) => {
  const dates = []
  const values = []
  for (let i = 6; i >= 0; i--) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    dates.push(date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' }))
    values.push(Math.max(0, Math.min(100, baseValue + Math.random() * 20 - 10)))
  }
  return { dates, values }
}

const knowledgeData = generateTrendData(75, '知识点掌握度')
const answerData = generateTrendData(78, '答题正确率')
const progressData = generateTrendData(70, '学习进度')
const abilityData = generateTrendData(12, '能力提升')

const buildLineChartOption = (data: { dates: string[], values: number[] }, name: string, max: number = 100) => {
  return {
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: data.dates
    },
    yAxis: {
      type: 'value',
      max: max
    },
    series: [{
      name: name,
      type: 'line',
      smooth: true,
      areaStyle: {
        color: 'rgba(59, 130, 246, 0.3)'
      },
      lineStyle: {
        color: '#3b82f6',
        width: 2
      },
      itemStyle: {
        color: '#3b82f6'
      },
      data: data.values
    }]
  }
}

const knowledgeMasteryOption = computed<EChartsOption>(() => 
  buildLineChartOption(knowledgeData, '知识点掌握度', 10)
)

const answerAccuracyOption = computed<EChartsOption>(() => 
  buildLineChartOption(answerData, '答题正确率', 100)
)

const progressCompletionOption = computed<EChartsOption>(() => 
  buildLineChartOption(progressData, '学习进度完成率', 100)
)

const abilityImprovementOption = computed<EChartsOption>(() => 
  buildLineChartOption(abilityData, '能力提升幅度', 30)
)

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const generateEvaluation = async () => {
  if (!userStore.userInfo?.userId) return
  
  isGenerating.value = true
  
  try {
    const res = await evaluationApi.generate({
      userId: userStore.userInfo.userId,
      evaluationPeriod: '2026年第14周'
    })
    recentEvaluations.value.unshift(res.data)
  } catch (error) {
    console.error('生成评估报告失败:', error)
  } finally {
    isGenerating.value = false
  }
}

const loadDashboard = async () => {
  if (!userStore.userInfo?.userId) return
  
  try {
    const res = await evaluationApi.dashboard(userStore.userInfo.userId)
    recentEvaluations.value = res.data.recentEvaluations || []
    knowledgeGaps.value = res.data.knowledgeGaps || []
  } catch (error) {
    console.error('加载看板数据失败:', error)
  }
}

onMounted(() => {
  if (!userStore.token) {
    router.push('/login')
    return
  }
  loadDashboard()
})
</script>
