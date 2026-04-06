import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import { hasPermission, hasRole, hasAnyPermission, hasAnyRole } from './directives/permission'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.directive('permission', hasPermission)
app.directive('role', hasRole)
app.directive('any-permission', hasAnyPermission)
app.directive('any-role', hasAnyRole)

app.mount('#app')
