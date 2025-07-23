<template>
  <div class="admin-layout">
    <!-- ===== SIDEBAR ===== -->
    <aside class="sidebar">
      <h2 class="logo">InsightViz</h2>

      <button class="sidebar-btn" @click="current = 'dashboard'">
        Tableau de bord
      </button>

      <div class="dropdown">
        <label for="param">Paramètre</label>
        <div class="select-wrapper">
          <select id="param" v-model="selected" @change="change">
            <option disabled value="">— Choisir —</option>
            <option value="user">👤 Utilisateur</option>
            <option value="enquete">📋 Enquête</option>
            <option value="reponse">📝 Réponse</option>
            <option value="campagne">📢 Campagne</option>
          </select>

          <!-- Icônes à droite du select -->
          <span class="icon">
            <svg v-if="selected==='user'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" viewBox="0 0 24 24"><path d="M12 12c2.7 0 5-2.3 5-5s-2.3-5-5-5-5 2.3-5 5 2.3 5 5 5zm0 2c-3.3 0-10 1.7-10 5v3h20v-3c0-3.3-6.7-5-10-5z"/></svg>
            <svg v-else-if="selected==='enquete'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" viewBox="0 0 24 24"><path d="M3 4v16h18V4H3zm16 14H5V6h14v12z"/><path d="M7 8h10v2H7zm0 4h6v2H7z"/></svg>
            <svg v-else-if="selected==='reponse'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" viewBox="0 0 24 24"><path d="M21 6h-2V4H5v2H3v14h18V6zM5 8h14v10H5V8z"/></svg>
            <svg v-else-if="selected==='campagne'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" viewBox="0 0 24 24"><path d="M21 4v13h-4v3l-5-3h-8V4h17zm-2 2H5v9h5l4 2.5V15h5V6z"/></svg>
          </span>
        </div>
      </div>
    </aside>

    <!-- ===== ZONE BLANCHE – composant dynamique ===== -->
    <main class="content">
      <component :is="componentMap[current]" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AdminHome from './AdminHome.vue'
import UserForm from './UserForm.vue'
import EqueteForm from './EqueteForm.vue'
import ReponseForm from './ReponseForm.vue'
import CampagneForm from './CampagneForm.vue'

const current = ref('dashboard')
const selected = ref('')

const componentMap = {
  dashboard: AdminHome,
  user: UserForm,
  enquete: EqueteForm,
  reponse: ReponseForm,
  campagne: CampagneForm
}

const change = () => {
  if (selected.value) {
    current.value = selected.value
    selected.value = ''
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 260px;
  height: 100vh;
  padding: 2rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  background: linear-gradient(135deg, #372d67 0%, #6a11cb 60%, #2575fc 100%);
  color: #fff;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.15);
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 1rem;
}

.sidebar-btn {
  background: #fff;
  color: #6a11cb;
  border: none;
  padding: 0.7rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}
.sidebar-btn:hover {
  opacity: 0.9;
}

.dropdown label {
  display: block;
  margin-bottom: 0.35rem;
  font-size: 0.95rem;
}

/* Select + icône à droite */
.select-wrapper {
  position: relative;
}
.select-wrapper select {
  width: 100%;
  padding: 0.55rem 2rem 0.55rem 0.75rem;
  border-radius: 6px;
  border: none;
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  appearance: none;
}
.select-wrapper .icon {
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  pointer-events: none;
}

.content {
  margin-left: 260px;
  height: 100vh;
  overflow-y: auto;
  background: #f9f9fe;
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
}
</style>
