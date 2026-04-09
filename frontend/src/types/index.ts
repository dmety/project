export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface UserInfo {
  userId: number
  username: string
  major?: string
  grade?: string
  createdAt: string
  lastLoginAt: string
  status: number
}

export interface LoginParams {
  username: string
  password: string
}

export interface LoginResponse {
  token: string
  user_id: number
  username: string
  roles: string[]
  permissions: string[]
}

export interface Role {
  roleId: number
  roleName: string
  roleCode: string
  roleType: string
  roleDesc?: string
  sortOrder: number
  status: number
  createdAt: string
  updatedAt: string
}

export interface Permission {
  permissionId: number
  permissionName: string
  permissionCode: string
  permissionType: string
  parentId: number
  routePath?: string
  componentPath?: string
  icon?: string
  sortOrder: number
  status: number
  createdAt: string
}

export interface OperationLog {
  logId: number
  userId?: number
  roleCode?: string
  module?: string
  operationType?: string
  requestUrl?: string
  requestMethod?: string
  requestParams?: string
  responseResult?: string
  operationIp?: string
  operationTime: string
  duration?: number
  status: number
  errorMsg?: string
}

export interface ProfileDimension {
  knowledgeLevel?: number
  cognitiveStyle?: string
  knowledgeWeakness: string[]
  errorPronePoints: string[]
  learningGoals?: string
  learningPace?: string
  interestDirections: string[]
  learningBehavior?: string
}

export interface ChatMessageItem {
  role: 'user' | 'assistant'
  content: string
}

export interface ProfileDialogRequest {
  userId: number
  message: string
  conversationId?: string
  history?: ChatMessageItem[]
}

export interface ProfileDialogResponse {
  conversationId: string
  assistantMessage: string
  extractedFeatures?: Record<string, any>
}

export interface ProfileUpdateRequest {
  userId: number
  dimensions: ProfileDimension
}

export interface ProfileVisualizationData {
  userId: number
  radarData: Record<string, number>
  heatmapData: number[][]
  dimensionDetails: ProfileDimension
  updatedAt: string
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}

export interface ResourceType {
  COURSE_DOC: 'course_doc'
  MIND_MAP: 'mind_map'
  EXERCISE: 'exercise'
  CODE_CASE: 'code_case'
  EXTENSION_READING: 'extension_reading'
  MULTIMODAL_DIAGRAM: 'multimodal_diagram'
}

export interface DifficultyLevel {
  EASY: 'easy'
  MEDIUM: 'medium'
  HARD: 'hard'
}

export interface ResourceGenerateRequest {
  userId: number
  knowledgeId: number
  resourceType: string
  difficulty: string
  enableAgent?: boolean
}

export interface ResourceResponse {
  resourceId: number
  userId: number
  knowledgeId: number
  resourceType: string
  resourceContent: string
  generatedAt: string
  usageStatus: number
  isCompliant: boolean
}

export interface LearningPathNode {
  nodeId: number
  pathId: number
  knowledgeId: number
  learningOrder: number
  milestoneFlag: boolean
  learningContent?: string
  completionStatus: number
  planCompletionTime?: string
  actualCompletionTime?: string
}

export interface LearningPathResponse {
  pathId: number
  userId: number
  pathName: string
  learningCycle?: number
  totalMilestones: number
  completedMilestones: number
  currentProgress: number
  status: number
  createdAt: string
  updatedAt?: string
  nodes: LearningPathNode[]
}

export interface TutorDialogRequest {
  userId: number
  question: string
  questionType?: string
  codeContent?: string
  imageUrl?: string
  conversationId?: string
  enableAgent?: boolean
}

export interface TutorDialogResponse {
  conversationId: string
  answer: string
  answerType: string
  codeSuggestion?: string
  diagramUrl?: string
  relatedExercises: number[]
}

export interface RunCodeResponse {
  success: boolean
  output?: string
  errors?: string
}

export interface ResourcePushItem {
  resourceId: number
  resourceType: string
  knowledgeId: number
  readStatus: number
  pushedAt: string
}
