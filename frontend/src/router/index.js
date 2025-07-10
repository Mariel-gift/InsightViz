import { createRouter, createWebHistory } from 'vue-router'

import Dashboard from '../components/Dashboard.vue'
import AuthSystem from '../components/AuthSystem.vue'
import UserForm from '../components/UserForm.vue'
const routes = [
  { path: '/', name: 'Login', component: AuthSystem },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  {path: '/user', name: 'UserForm', component: UserForm },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
