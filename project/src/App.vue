<template>
  <div id="app" class="app">
    <Header 
      :user="currentUser" 
      @toggleSidebar="toggleSidebar"
      @logout="handleLogout"
      @showProfile="showUserProfile = true"
    />
    
    <div class="app-content">
      <Sidebar 
        :isOpen="sidebarOpen"
        :activeSection="activeSection"
        @navigate="handleNavigation"
        @closeSidebar="closeSidebar"
      />
      
      <main class="main-content" :class="{ 'sidebar-open': sidebarOpen }">
        <Dashboard v-if="activeSection === 'dashboard'" />
        <Users v-else-if="activeSection === 'users'" />
        <Surveys v-else-if="activeSection === 'surveys'" />
        <Responses v-else-if="activeSection === 'responses'" />
        <Campaigns v-else-if="activeSection === 'campaigns'" />
        <Persons v-else-if="activeSection === 'persons'" />
      </main>
    </div>

    <!-- Overlay pour mobile -->
    <div 
      v-if="sidebarOpen" 
      class="sidebar-overlay"
      @click="closeSidebar"
    ></div>

    <!-- Modal profil utilisateur -->
    <div v-if="showUserProfile" class="modal-overlay" @click="showUserProfile = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Profil Utilisateur</h3>
          <button @click="showUserProfile = false" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="profile-info">
            <div class="profile-avatar">
              <img :src="currentUser.avatar" :alt="currentUser.name" />
            </div>
            <div class="profile-details">
              <h4>{{ currentUser.name }}</h4>
              <p>{{ currentUser.email }}</p>
              <p>{{ currentUser.role }}</p>
              <p>Membre depuis: {{ currentUser.joinDate }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Header from './components/Header.vue'
import Sidebar from './components/Sidebar.vue'
import Dashboard from './components/Dashboard.vue'
import Users from './components/Users.vue'
import Surveys from './components/Surveys.vue'
import Responses from './components/Responses.vue'
import Campaigns from './components/Campaigns.vue'
import Persons from './components/Persons.vue'

const sidebarOpen = ref(false)
const activeSection = ref('dashboard')
const showUserProfile = ref(false)

const currentUser = ref({
  name: 'Marie Dubois',
  email: 'marie.dubois@insightviz.fr',
  role: 'Administrateur',
  joinDate: '15 Mars 2024',
  avatar: 'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=150'
})

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const closeSidebar = () => {
  sidebarOpen.value = false
}

const handleNavigation = (section: string) => {
  activeSection.value = section
  if (window.innerWidth < 768) {
    closeSidebar()
  }
}

const handleLogout = () => {
  alert('Déconnexion effectuée!')
}

onMounted(() => {
  // Fermer la sidebar sur desktop par défaut
  if (window.innerWidth >= 768) {
    sidebarOpen.value = true
  }
})
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8fafc;
}

.app-content {
  display: flex;
  flex: 1;
  position: relative;
}

.main-content {
  flex: 1;
  padding: 2rem;
  margin-left: 0;
  transition: margin-left 0.3s ease;
  overflow-x: auto;
}

.main-content.sidebar-open {
  margin-left: 280px;
}

.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 40;
  display: none;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 0;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.25rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: #f3f4f6;
}

.modal-body {
  padding: 1.5rem;
}

.profile-info {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.profile-avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-details h4 {
  margin: 0 0 0.5rem 0;
  color: #1f2937;
  font-size: 1.25rem;
  font-weight: 600;
}

.profile-details p {
  margin: 0.25rem 0;
  color: #6b7280;
}

@media (max-width: 767px) {
  .main-content.sidebar-open {
    margin-left: 0;
  }
  
  .sidebar-overlay {
    display: block;
  }
  
  .profile-info {
    flex-direction: column;
    text-align: center;
  }
}
</style>