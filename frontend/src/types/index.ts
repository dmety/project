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
  userInfo: UserInfo
}
