import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import type { LoginResponse } from '@/types'

const TOKEN_KEY = 'token'
const USER_KEY = 'user'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>('')
  const userId = ref<number>(0)
  const username = ref<string>('')
  const roles = ref<string[]>([])
  const permissions = ref<string[]>([])

  const initFromStorage = () => {
    const savedToken = localStorage.getItem(TOKEN_KEY)
    const savedUser = localStorage.getItem(USER_KEY)
    if (savedToken) {
      token.value = savedToken
    }
    if (savedUser) {
      try {
        const userData = JSON.parse(savedUser)
        userId.value = userData.userId || 0
        username.value = userData.username || ''
        roles.value = userData.roles || []
        permissions.value = userData.permissions || []
      } catch {
        console.error('Failed to parse user data from localStorage')
      }
    }
  }

  const setAuthData = (data: LoginResponse) => {
    token.value = data.token
    userId.value = data.user_id
    username.value = data.username
    roles.value = data.roles
    permissions.value = data.permissions
  }

  const saveToStorage = () => {
    if (token.value) {
      localStorage.setItem(TOKEN_KEY, token.value)
    } else {
      localStorage.removeItem(TOKEN_KEY)
    }
    const userData = {
      userId: userId.value,
      username: username.value,
      roles: roles.value,
      permissions: permissions.value
    }
    if (userId.value) {
      localStorage.setItem(USER_KEY, JSON.stringify(userData))
    } else {
      localStorage.removeItem(USER_KEY)
    }
  }

  const hasRole = (roleCode: string): boolean => {
    return roles.value.includes(roleCode) || roles.value.includes('super_admin')
  }

  const hasAnyRole = (roleCodes: string[]): boolean => {
    return roleCodes.some(code => hasRole(code))
  }

  const hasPermission = (permissionCode: string): boolean => {
    if (roles.value.includes('super_admin')) return true
    return permissions.value.includes(permissionCode)
  }

  const hasAnyPermission = (permissionCodes: string[]): boolean => {
    return permissionCodes.some(code => hasPermission(code))
  }

  const hasAllPermissions = (permissionCodes: string[]): boolean => {
    return permissionCodes.every(code => hasPermission(code))
  }

  const logout = () => {
    token.value = ''
    userId.value = 0
    username.value = ''
    roles.value = []
    permissions.value = []
  }

  initFromStorage()
  watch([token, userId, username, roles, permissions], saveToStorage)

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
