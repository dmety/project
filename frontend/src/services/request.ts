import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios'

const TOKEN_KEY = 'token'

const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000
})

service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem(TOKEN_KEY)
    if (token && config.headers) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  (response: AxiosResponse) => {
    const res = response.data
    console.log('响应拦截器 - 原始响应:', response)
    console.log('响应拦截器 - 响应数据:', res)
    if (res.code !== 200) {
      console.error('请求错误:', res.message)
      return Promise.reject(new Error(res.message || '请求错误'))
    }
    return res
  },
  (error) => {
    console.error('响应错误:', error)
    return Promise.reject(error)
  }
)

export default service
