<template>
  <div class="flex h-screen bg-gray-50">
    <div class="w-1/2 flex flex-col border-r border-gray-200">
      <div class="bg-white p-4 border-b border-gray-200">
        <h2 class="text-xl font-bold text-gray-800">多模态智能辅导</h2>
        <p class="text-sm text-gray-500">文字、图片、代码多种形式提问</p>
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
        <div class="space-y-3">
          <textarea v-model="inputMessage"
                    @keydown.enter.prevent="sendMessage"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="输入您的问题..."
                    rows="3"></textarea>
          <div class="flex space-x-2">
            <button @click="sendMessage"
                    :disabled="!inputMessage.trim() || isLoading"
                    class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed">
              发送
            </button>
            <button class="px-4 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg">
              上传图片
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="w-1/2 flex flex-col">
      <div class="bg-white p-4 border-b border-gray-200">
        <h2 class="text-xl font-bold text-gray-800">Python 代码编辑器</h2>
        <p class="text-sm text-gray-500">在线编写、运行代码</p>
      </div>
      
      <div class="flex-1 flex flex-col p-4">
        <textarea v-model="codeContent"
                  class="flex-1 bg-gray-900 text-gray-100 font-mono text-sm p-4 rounded-lg resize-none focus:outline-none"
                  placeholder="# 在这里编写 Python 代码
print('Hello, World!')"></textarea>
        
        <div class="mt-4 bg-gray-900 text-gray-100 p-4 rounded-lg min-h-32">
          <div class="flex justify-between items-center mb-2">
            <span class="text-sm font-medium text-gray-400">输出结果</span>
            <button @click="runCode"
                    :disabled="isRunning"
                    class="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700 disabled:opacity-50">
              {{ isRunning ? '运行中...' : '运行代码' }}
            </button>
          </div>
          <pre class="whitespace-pre-wrap">{{ codeOutput }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { marked } from 'marked'
import { tutorApi } from '@/services/api'
import type { ChatMessage } from '@/types'

const router = useRouter()
const userStore = useUserStore()
const chatContainer = ref<HTMLElement>()

const messages = ref<ChatMessage[]>([
  {
    role: 'assistant',
    content: '您好！我是您的智能学习辅导助手。您可以通过文字、图片或代码的形式向我提问，我会尽力为您解答！\n\n**支持的功能：\n- Python代码运行与调试\n- 知识点讲解\n- 错题分析\n- 代码优化建议'
  }
])
const inputMessage = ref('')
const isLoading = ref(false)
const conversationId = ref<string>()

const codeContent = ref(`# 在这里编写 Python 代码
print('Hello, World!')
`)
const codeOutput = ref('')
const isRunning = ref(false)

const renderMarkdown = (content: string | null | undefined) => {
  if (!content) return ''
  return marked(content)
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
    const res = await tutorApi.dialog({
      userId: userStore.userId,
      question: message,
      conversationId: conversationId.value
    })
    
    const data = res.data as any
    conversationId.value = data.conversationId
    messages.value.push({
      role: 'assistant',
      content: data.answer
    })
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

const runCode = async () => {
  if (!userStore.userId || isRunning.value) return
  
  isRunning.value = true
  codeOutput.value = '正在运行...'
  
  try {
    const res = await tutorApi.runCode({
      userId: userStore.userId,
      codeContent: codeContent.value
    })
    
    const data = res.data as any
    if (data.success) {
      codeOutput.value = data.output || '执行成功，无输出'
    } else {
      codeOutput.value = data.errors || '执行失败'
    }
  } catch (error) {
    console.error('运行代码失败:', error)
    codeOutput.value = '代码运行时发生错误'
  } finally {
    isRunning.value = false
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
