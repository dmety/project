import type { Directive, DirectiveBinding } from 'vue'
import { useUserStore } from '@/store/user'

export const hasPermission: Directive = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const userStore = useUserStore()
    const permission = binding.value
    
    if (permission && !userStore.hasPermission(permission)) {
      el.parentNode?.removeChild(el)
    }
  }
}

export const hasRole: Directive = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const userStore = useUserStore()
    const role = binding.value
    
    if (role && !userStore.hasRole(role)) {
      el.parentNode?.removeChild(el)
    }
  }
}

export const hasAnyPermission: Directive = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const userStore = useUserStore()
    const permissions = binding.value
    
    if (permissions && Array.isArray(permissions) && !userStore.hasAnyPermission(permissions)) {
      el.parentNode?.removeChild(el)
    }
  }
}

export const hasAnyRole: Directive = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const userStore = useUserStore()
    const roles = binding.value
    
    if (roles && Array.isArray(roles) && !userStore.hasAnyRole(roles)) {
      el.parentNode?.removeChild(el)
    }
  }
}
