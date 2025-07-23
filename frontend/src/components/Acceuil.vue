<template>
  <div class="home-container">
    <div class="home-content">
      <h1 class="title">Bienvenue sur <span>InsightViz</span></h1>
      <p class="subtitle">Système d’analyse automatisée et de visualisation des données d’enquêtes logistiques.</p>
      <router-link to="/dashboard">
        <button class="cta-button">Accéder au Dashboard</button>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Accueil'
}
</script>

<style scoped>
.home-container {
  width: 100%;
  height: 100vh;
  background: linear-gradient(135deg, #6a11cb, #1567f5);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.home-content {
  text-align: center;
  padding: 2rem;
}

.title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.title span {
  color: #ffffff;
  background: linear-gradient(to right, #a18cd1, #fbc2eb);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: 1.25rem;
  margin-bottom: 2rem;
}

.cta-button {
  background-color: white;
  color: #6a11cb;
  padding: 0.75rem 2rem;
  font-size: 1rem;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cta-button:hover {
  background-color: #f0f0f0;
}
</style>
