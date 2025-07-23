<template>
  <section class="apropos-container">
    <h2 class="title">Pourquoi choisir InsightViz&nbsp;?</h2>

    <div class="grid-box">
      <div class="card">
        <div class="icon">📊</div>
        <h3>Analyse automatisée</h3>
        <p>
          InsightViz vous aide à automatiser l’analyse de vos enquêtes logistiques,
          en fournissant des statistiques et graphiques prêts à l’emploi.
        </p>
      </div>

      <div class="card">
        <div class="icon">🛡️</div>
        <h3>Plateforme sécurisée</h3>
        <p>
          Toutes les données sont traitées de façon sécurisée via Flask, PostgreSQL
          et SQLAlchemy. Aucun risque de perte ou de fuite.
        </p>
      </div>

      <div class="card">
        <div class="icon">⚡</div>
        <h3>Visualisation rapide</h3>
        <p>
          Grâce à Vue.js et Chart.js, obtenez une visualisation rapide,
          claire et dynamique de vos campagnes en temps réel.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
// aucun script pour l’instant (statique)
</script>

<style scoped>
.apropos-container {
  max-width: 1200px;
  margin: 4rem auto;
  padding: 2rem;
  text-align: center;
}

.title {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 2.5rem;
}

/* Grille 3 colonnes */
.grid-box {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 2rem;
}

.card {
  background: #fff;
  border-radius: 12px;
  padding: 1.8rem 1.5rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

.icon {
  font-size: 2.5rem;
  color: #2575fc;
  margin-bottom: 1rem;
}

.card h3 {
  font-size: 1.2rem;
  color: #2c3e50;
  margin-bottom: 0.8rem;
}

.card p {
  font-size: 0.95rem;
  color: #555;
  line-height: 1.5;
}
</style>
