import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { LoginResponse } from '@/types'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>('')
  const userId = ref<number>(0)
  const username = ref<string>('')
  const roles = ref<string[]>([])
  const permissions = ref<string[]>([])

  const setAuthData = (data: LoginResponse) => {
    token.value = data.token
    userId.value = data.user_id
    username.value = data.username
    roles.value = data.roles
    permissions.value = data.permissions
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
