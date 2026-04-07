
content = '''import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { LoginResponse } from '@/types'

const TOKEN_KEY = 'token'
const USER_KEY = 'user'

export const useUserStore = defineStore('user', () => {
  const token = ref('')
  const userId = ref(0)
  const username = ref('')
  const roles = ref([])
  const permissions = ref([])

  const saveToStorage = () => {
    try {
      if (token.value) {
        localStorage.setItem(TOKEN_KEY, token.value)
      } else {
        localStorage.removeItem(TOKEN_KEY)
      }
      
      if (userId.value > 0) {
        const userData = {
          userId: userId.value,
          username: username.value,
          roles: roles.value,
          permissions: permissions.value
        }
        localStorage.setItem(USER_KEY, JSON.stringify(userData))
      } else {
        localStorage.removeItem(USER_KEY)
      }
    } catch (error) {
      console.error('Save error:', error)
    }
  }

  const initFromStorage = () => {
    try {
      const savedToken = localStorage.getItem(TOKEN_KEY)
      const savedUser = localStorage.getItem(USER_KEY)
      
      if (savedToken && savedToken !== 'undefined' && savedToken !== 'null') {
        token.value = savedToken
      }
      
      if (savedUser && savedUser !== 'undefined' && savedUser !== 'null') {
        try {
          const userData = JSON.parse(savedUser)
          if (userData) {
            userId.value = userData.userId || 0
            username.value = userData.username || ''
            roles.value = Array.isArray(userData.roles) ? userData.roles : []
            permissions.value = Array.isArray(userData.permissions) ? userData.permissions : []
          }
        } catch {
          console.error('Parse error')
        }
      }
    } catch (error) {
      console.error('Init error:', error)
    }
  }

  const setAuthData = (data: LoginResponse) => {
    token.value = data.token
    userId.value = data.user_id
    username.value = data.username
    roles.value = data.roles
    permissions.value = data.permissions
    saveToStorage()
  }

  const hasRole = (roleCode: string): boolean => {
    if (!roles.value) return false
    return roles.value.includes(roleCode) || roles.value.includes('super_admin')
  }

  const hasAnyRole = (roleCodes: string[]): boolean => {
    if (!roleCodes || !Array.isArray(roleCodes)) return false
    return roleCodes.some(code => hasRole(code))
  }

  const hasPermission = (permissionCode: string): boolean => {
    if (!permissions.value) return false
    if (roles.value && roles.value.includes('super_admin')) return true
    return permissions.value.includes(permissionCode)
  }

  const hasAnyPermission = (permissionCodes: string[]): boolean => {
    if (!permissionCodes || !Array.isArray(permissionCodes)) return false
    return permissionCodes.some(code => hasPermission(code))
  }

  const hasAllPermissions = (permissionCodes: string[]): boolean => {
    if (!permissionCodes || !Array.isArray(permissionCodes)) return false
    return permissionCodes.every(code => hasPermission(code))
  }

  const logout = () => {
    token.value = ''
    userId.value = 0
    username.value = ''
    roles.value = []
    permissions.value = []
    saveToStorage()
  }

  initFromStorage()

  return {
    token,
    userId,
    username,
    roles,
    permissions,
    setAuthData,
    hasRole,
    hasAnyRole,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    logout
  }
})
'''

with open(r'e:\Users\HUAWEI\Desktop\project\frontend\src\store\user.ts', 'w', encoding='utf-8') as f:
    f.write(content)

print('File created successfully!')

