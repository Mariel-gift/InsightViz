<template>
  <aside class="sidebar" :class="{ 'sidebar-open': isOpen }">
    <nav class="nav">
      <div class="nav-section">
        <h3 class="nav-title">Navigation</h3>
        <ul class="nav-list">
          <li>
            <button 
              @click="$emit('navigate', 'dashboard')"
              class="nav-item"
              :class="{ active: activeSection === 'dashboard' }"
            >
              <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v6a2 2 0 01-2 2H10a2 2 0 01-2-2V5z"></path>
              </svg>
              Tableau de bord
            </button>
          </li>
          <li>
            <button 
              @click="$emit('navigate', 'users')"
              class="nav-item"
              :class="{ active: activeSection === 'users' }"
            >
              <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
              </svg>
              Utilisateurs
            </button>
          </li>
          <li>
            <button 
              @click="$emit('navigate', 'surveys')"
              class="nav-item"
              :class="{ active: activeSection === 'surveys' }"
            >
              <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
              </svg>
              Enquêtes
            </button>
          </li>
          <li>
            <button 
              @click="$emit('navigate', 'responses')"
              class="nav-item"
              :class="{ active: activeSection === 'responses' }"
            >
              <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
              </svg>
              Réponses
            </button>
          </li>
          <li>
            <button 
              @click="$emit('navigate', 'campaigns')"
              class="nav-item"
              :class="{ active: activeSection === 'campaigns' }"
            >
              <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path>
              </svg>
              Campagnes
            </button>
          </li>
          <li>
            <button 
              @click="$emit('navigate', 'persons')"
              class="nav-item"
              :class="{ active: activeSection === 'persons' }"
            >
              <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
              Personnes
            </button>
          </li>
        </ul>
      </div>
    </nav>
  </aside>
</template>

<script setup lang="ts">
defineProps<{
  isOpen: boolean
  activeSection: string
}>()

defineEmits<{
  navigate: [section: string]
  closeSidebar: []
}>()
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 73px;
  bottom: 0;
  width: 280px;
  background: white;
  border-right: 1px solid #e5e7eb;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  z-index: 20;
  overflow-y: auto;
}

.sidebar-open {
  transform: translateX(0);
}

.nav {
  padding: 2rem 0;
}

.nav-section {
  margin-bottom: 2rem;
}

.nav-title {
  padding: 0 1.5rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.nav-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.875rem 1.5rem;
  border: none;
  background: none;
  text-align: left;
  font-size: 0.95rem;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background-color: #f9fafb;
  color: #1f2937;
}

.nav-item.active {
  background-color: #eff6ff;
  color: #3b82f6;
  border-left-color: #3b82f6;
}

.nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

@media (min-width: 768px) {
  .sidebar {
    position: relative;
    top: 0;
    transform: none;
  }
}
</style>