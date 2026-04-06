import request from './request'
import type {
  ApiResponse,
  ProfileDialogRequest,
  ProfileDialogResponse,
  ProfileUpdateRequest,
  ProfileVisualizationData,
  ResourceGenerateRequest,
  ResourceResponse,
  TutorDialogRequest,
  TutorDialogResponse
} from '@/types'

export const authApi = {
  login: (data: { username: string; password: string }) =>
    request.post<ApiResponse<any>>('/auth/login', data),
  register: (data: { username: string; password: string; major?: string; grade?: string }) =>
    request.post<ApiResponse<any>>('/auth/register', data)
}

export const profileApi = {
  dialog: (data: ProfileDialogRequest) =>
    request.post<ApiResponse<ProfileDialogResponse>>('/profile/dialog', {
      user_id: data.userId,
      message: data.message,
      conversation_id: data.conversationId
    }),
  update: (data: ProfileUpdateRequest) =>
    request.post<ApiResponse<any>>('/profile/update', {
      user_id: data.userId,
      dimensions: {
        knowledge_level: data.dimensions.knowledgeLevel,
        cognitive_style: data.dimensions.cognitiveStyle,
        knowledge_weakness: data.dimensions.knowledgeWeakness,
        error_prone_points: data.dimensions.errorPronePoints,
        learning_goals: data.dimensions.learningGoals,
        learning_pace: data.dimensions.learningPace,
        interest_directions: data.dimensions.interestDirections,
        learning_behavior: data.dimensions.learningBehavior
      }
    }),
  getVisualization: (userId: number) =>
    request.get<ApiResponse<ProfileVisualizationData>>(`/profile/visualization/${userId}`)
}

export const resourceApi = {
  generate: (data: ResourceGenerateRequest) =>
    request.post<ApiResponse<ResourceResponse>>('/resource/generate', {
      user_id: data.userId,
      knowledge_id: data.knowledgeId,
      resource_type: data.resourceType,
      difficulty: data.difficulty,
      enable_agent: data.enableAgent
    }),
  list: (params: { userId: number; knowledgeId?: number; resourceType?: string; page?: number; pageSize?: number }) =>
    request.get<ApiResponse<any>>('/resource/list', {
      params: {
        user_id: params.userId,
        knowledge_id: params.knowledgeId,
        resource_type: params.resourceType,
        page: params.page || 1,
        page_size: params.pageSize || 10
      }
    }),
  detail: (resourceId: number) =>
    request.get<ApiResponse<ResourceResponse>>(`/resource/detail/${resourceId}`),
  feedback: (data: { resourceId: number; userId: number; rating: number; feedback?: string }) =>
    request.post<ApiResponse<any>>('/resource/feedback', {
      resource_id: data.resourceId,
      user_id: data.userId,
      rating: data.rating,
      feedback: data.feedback
    })
}

export const pathApi = {
  generate: (data: { userId: number; pathName: string; startKnowledgeId?: number; targetKnowledgeId?: number; enableAgent?: boolean }) =>
    request.post<ApiResponse<any>>('/path/generate', {
      user_id: data.userId,
      path_name: data.pathName,
      start_knowledge_id: data.startKnowledgeId,
      target_knowledge_id: data.targetKnowledgeId,
      enable_agent: data.enableAgent
    }),
  list: (userId: number) =>
    request.get<ApiResponse<any>>(`/path/list/${userId}`),
  detail: (pathId: number) =>
    request.get<ApiResponse<any>>(`/path/detail/${pathId}`),
  updateNode: (data: { nodeId: number; completionStatus?: number; learningContent?: string }) =>
    request.post<ApiResponse<any>>('/path/node/update', {
      node_id: data.nodeId,
      completion_status: data.completionStatus,
      learning_content: data.learningContent
    }),
  push: (data: { userId: number; pathId?: number; nodeId?: number; knowledgeId?: number }) =>
    request.post<ApiResponse<any>>('/path/push', {
      user_id: data.userId,
      path_id: data.pathId,
      node_id: data.nodeId,
      knowledge_id: data.knowledgeId
    })
}

export const tutorApi = {
  dialog: (data: TutorDialogRequest) =>
    request.post<ApiResponse<TutorDialogResponse>>('/tutor/dialog', {
      user_id: data.userId,
      question: data.question,
      question_type: data.questionType,
      code_content: data.codeContent,
      image_url: data.imageUrl,
      conversation_id: data.conversationId,
      enable_agent: data.enableAgent
    }),
  runCode: (data: { userId: number; codeContent: string; language?: string }) =>
    request.post<ApiResponse<any>>('/tutor/code/run', {
      user_id: data.userId,
      code_content: data.codeContent,
      language: data.language || 'python'
    }),
  analyzeError: (data: { userId: number; exerciseId: number; userAnswer: string }) =>
    request.post<ApiResponse<any>>('/tutor/error/analysis', {
      user_id: data.userId,
      exercise_id: data.exerciseId,
      user_answer: data.userAnswer
    })
}

export const evaluationApi = {
  generate: (data: { userId: number; evaluationPeriod: string }) =>
    request.post<ApiResponse<any>>('/evaluation/generate', {
      user_id: data.userId,
      evaluation_period: data.evaluationPeriod
    }),
  dashboard: (userId: number) =>
    request.get<ApiResponse<any>>(`/evaluation/dashboard/${userId}`),
  checkSafety: (data: { content: string; contentType?: string; checkType?: string }) =>
    request.post<ApiResponse<any>>('/evaluation/safety/check', {
      content: data.content,
      content_type: data.contentType || 'text',
      check_type: data.checkType || 'all'
    }),
  ragRetrieve: (data: { query: string; topK?: number; knowledgeIds?: number[] }) =>
    request.post<ApiResponse<any>>('/evaluation/rag/retrieve', {
      query: data.query,
      top_k: data.topK || 5,
      knowledge_ids: data.knowledgeIds
    })
}
