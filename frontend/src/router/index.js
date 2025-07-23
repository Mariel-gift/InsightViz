import { createRouter, createWebHistory } from 'vue-router'

import Dashboard from '../components/Dashboard.vue'
import AuthSystem from '../components/AuthSystem.vue'
import UserForm from '../components/UserForm.vue'
import EqueteForm from '../components/EqueteForm.vue'
import ReponseForm from '../components/ReponseForm.vue'
import PersonneForm from '../components/PersonneForm.vue'
import CampagneForm from '../components/CampagneForm.vue'
import Back_Office from '../components/Back_Office.vue'
import AdminDashBoard from '../components/AdminDashBoard.vue'

const routes = [
  { path: '/', name: 'Login', component: AuthSystem },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  {path: '/user', name: 'UserForm', component: UserForm },
  {path: '/equete', name: 'EqueteForm', component: EqueteForm },
  {path: '/reponse', name: 'ReponseForm', component: ReponseForm },
  {path: '/personne', name: 'PersonneForm', component: PersonneForm },
  {path: '/campagne/', name: 'CampagneForm', component: CampagneForm },
  {path: '/back-office', name: 'BackOffice', component: Back_Office },
  {path: '/admin', name: 'AdminDashBoard', component: AdminDashBoard },
  { path: '/campagne/edit/:id', name: 'EditCampagne', component: CampagneForm, props: true }


]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
