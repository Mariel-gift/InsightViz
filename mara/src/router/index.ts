import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import UserView from '../views/UserView.vue'
import SurveyView from '../views/SurveyView.vue'
import ResponseView from '../views/ResponseView.vue'
import CampaignView from '../views/CampaignView.vue'
import PersonView from '../views/PersonView.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/user',
    name: 'User',
    component: UserView
  },
  {
    path: '/survey',
    name: 'Survey', 
    component: SurveyView
  },
  {
    path: '/response',
    name: 'Response',
    component: ResponseView
  },
  {
    path: '/campaign',
    name: 'Campaign',
    component: CampaignView
  },
  {
    path: '/person',
    name: 'Person',
    component: PersonView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router