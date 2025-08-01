<template>
  <div class="sidebar">
    <div class="logo-container">
      <h1 class="logo">InsightViz</h1>
    </div>
    
    <nav class="nav-menu">
      <router-link 
        v-for="item in menuItems" 
        :key="item.name"
        :to="item.path"
        class="nav-item"
        :class="{ 'active': $route.path === item.path }"
      >
        <component :is="item.icon" class="nav-icon" />
        <span class="nav-text">{{ item.name }}</span>
      </router-link>
    </nav>

    <div class="user-section">
      <div class="user-profile">
        <div class="user-avatar">
          <UserIcon class="avatar-icon" />
        </div>
        <div class="user-info">
          <p class="user-name">{{ currentUser.name }}</p>
          <p class="user-role">{{ currentUser.role }}</p>
        </div>
      </div>
      
      <button @click="showMembers = !showMembers" class="members-btn">
        <UsersIcon class="btn-icon" />
        Voir membres
      </button>
    </div>

    <!-- Modal des membres -->
    <div v-if="showMembers" class="modal-overlay" @click="showMembers = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Membres de l'équipe</h3>
          <button @click="showMembers = false" class="close-btn">
            <XMarkIcon class="close-icon" />
          </button>
        </div>
        <div class="members-list">
          <div v-for="member in teamMembers" :key="member.id" class="member-item">
            <div class="member-avatar">
              <UserIcon class="avatar-icon" />
            </div>
            <div class="member-info">
              <p class="member-name">{{ member.name }}</p>
              <p class="member-role">{{ member.role }}</p>
              <p class="member-email">{{ member.email }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UserIcon, UsersIcon, XMarkIcon, HomeIcon, DocumentTextIcon, ChatBubbleLeftRightIcon, SpeakerWaveIcon, UserGroupIcon } from '@heroicons/vue/24/outline'

const showMembers = ref(false)

const currentUser = {
  name: 'Marie Dubois',
  role: 'Administrateur',
  email: 'marie.dubois@insightviz.com'
}

const teamMembers = [
  { id: 1, name: 'Marie Dubois', role: 'Administrateur', email: 'marie.dubois@insightviz.com' },
  { id: 2, name: 'Jean Martin', role: 'Analyste', email: 'jean.martin@insightviz.com' },
  { id: 3, name: 'Sophie Laurent', role: 'Gestionnaire', email: 'sophie.laurent@insightviz.com' },
  { id: 4, name: 'Pierre Durand', role: 'Consultant', email: 'pierre.durand@insightviz.com' }
]

const menuItems = [
  { name: 'Utilisateur', path: '/user', icon: UserIcon },
  { name: 'Enquête', path: '/survey', icon: DocumentTextIcon },
  { name: 'Réponse', path: '/response', icon: ChatBubbleLeftRightIcon },
  { name: 'Campagne', path: '/campaign', icon: SpeakerWaveIcon },
  { name: 'Personne', path: '/person', icon: UserGroupIcon }
]
</script>

<style scoped>
.sidebar {
  width: 280px;
  height: 100vh;
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
  color: white;
  position: fixed;
  left: 0;
  top: 0;
  display: flex;
  flex-direction: column;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
}

.logo-container {
  padding: 2rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(45deg, #ffffff, #e0e7ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-menu {
  flex: 1;
  padding: 2rem 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.875rem 1.5rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border-left-color: #fbbf24;
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border-left-color: #10b981;
}

.nav-icon {
  width: 1.25rem;
  height: 1.25rem;
  margin-right: 0.75rem;
}

.nav-text {
  font-weight: 500;
}

.user-section {
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-profile {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  rounded: 0.5rem;
  border-radius: 0.5rem;
}

.user-avatar {
  width: 2.5rem;
  height: 2.5rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
}

.avatar-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.user-info {
  flex: 1;
}

.user-name {
  font-weight: 600;
  margin: 0;
  font-size: 0.875rem;
}

.user-role {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.members-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.members-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.btn-icon {
  width: 1rem;
  height: 1rem;
  margin-right: 0.5rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  color: #1f2937;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  transition: background 0.2s;
}

.close-btn:hover {
  background: #f3f4f6;
}

.close-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.member-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.5rem;
}

.member-avatar {
  width: 2.5rem;
  height: 2.5rem;
  background: #e5e7eb;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
}

.member-info {
  flex: 1;
}

.member-name {
  font-weight: 600;
  margin: 0 0 0.25rem 0;
}

.member-role {
  color: #6b7280;
  margin: 0 0 0.25rem 0;
  font-size: 0.875rem;
}

.member-email {
  color: #9ca3af;
  margin: 0;
  font-size: 0.75rem;
}
</style>