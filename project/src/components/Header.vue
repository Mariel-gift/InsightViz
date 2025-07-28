<template>
  <header class="header">
    <div class="header-left">
      <button @click="$emit('toggleSidebar')" class="menu-btn">
        <svg class="menu-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </button>
      <h1 class="logo">InsightViz</h1>
    </div>
    
    <div class="header-right">
      <div class="user-menu" @click="$emit('showProfile')">
        <img :src="user.avatar" :alt="user.name" class="user-avatar" />
        <span class="user-name">{{ user.name }}</span>
        <svg class="chevron-down" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
        </svg>
      </div>
      
      <button @click="$emit('logout')" class="logout-btn">
        <svg class="logout-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
        </svg>
        Déconnexion
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
defineProps<{
  user: {
    name: string
    email: string
    role: string
    joinDate: string
    avatar: string
  }
}>()

defineEmits<{
  toggleSidebar: []
  logout: []
  showProfile: []
}>()
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 30;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.menu-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 8px;
  color: #6b7280;
  transition: all 0.2s;
}

.menu-btn:hover {
  background-color: #f3f4f6;
  color: #1f2937;
}

.menu-icon {
  width: 24px;
  height: 24px;
}

.logo {
  font-size: 1.75rem;
  font-weight: 700;
  color: #3b82f6;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-menu:hover {
  background-color: #f3f4f6;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-weight: 500;
  color: #1f2937;
}

.chevron-down {
  width: 16px;
  height: 16px;
  color: #6b7280;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background-color: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.logout-btn:hover {
  background-color: #dc2626;
}

.logout-icon {
  width: 18px;
  height: 18px;
}

@media (max-width: 767px) {
  .header {
    padding: 1rem;
  }
  
  .user-name {
    display: none;
  }
  
  .logout-btn span {
    display: none;
  }
}
</style>