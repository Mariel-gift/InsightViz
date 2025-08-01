<template>
  <div class="app">
    <Sidebar />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import Sidebar from './components/Sidebar.vue'
</script>

<style scoped>
.app {
  display: flex;
  min-height: 100vh;
  background: #f8fafc;
}

.main-content {
  flex: 1;
  margin-left: 280px;
  min-height: 100vh;
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
}
</style>