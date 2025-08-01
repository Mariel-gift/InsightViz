<template>
  <div class="dashboard">
    <div class="welcome-section">
      <h1 class="welcome-title">Bienvenue sur InsightViz</h1>
      <p class="welcome-subtitle">Tableau de bord principal</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon survey">
          <DocumentTextIcon class="icon" />
        </div>
        <div class="stat-info">
          <h3 class="stat-number">24</h3>
          <p class="stat-label">Enquêtes actives</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon response">
          <ChatBubbleLeftRightIcon class="icon" />
        </div>
        <div class="stat-info">
          <h3 class="stat-number">1,285</h3>
          <p class="stat-label">Réponses collectées</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon campaign">
          <SpeakerWaveIcon class="icon" />
        </div>
        <div class="stat-info">
          <h3 class="stat-number">12</h3>
          <p class="stat-label">Campagnes en cours</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon person">
          <UserGroupIcon class="icon" />
        </div>
        <div class="stat-info">
          <h3 class="stat-number">847</h3>
          <p class="stat-label">Personnes enregistrées</p>
        </div>
      </div>
    </div>

    <div class="quick-actions">
      <h2 class="section-title">Actions rapides</h2>
      <div class="actions-grid">
        <router-link to="/survey" class="action-card">
          <DocumentTextIcon class="action-icon" />
          <h3>Créer une enquête</h3>
          <p>Lancez une nouvelle enquête</p>
        </router-link>

        <router-link to="/campaign" class="action-card">
          <SpeakerWaveIcon class="action-icon" />
          <h3>Nouvelle campagne</h3>
          <p>Démarrez une campagne</p>
        </router-link>

        <router-link to="/person" class="action-card">
          <UserGroupIcon class="action-icon" />
          <h3>Gérer les personnes</h3>
          <p>Administrez les contacts</p>
        </router-link>

        <router-link to="/response" class="action-card">
          <ChatBubbleLeftRightIcon class="action-icon" />
          <h3>Voir les réponses</h3>
          <p>Analysez les données</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DocumentTextIcon, ChatBubbleLeftRightIcon, SpeakerWaveIcon, UserGroupIcon } from '@heroicons/vue/24/outline'
</script>

<style scoped>
.dashboard {
  padding: 2rem;
}

.welcome-section {
  margin-bottom: 3rem;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.welcome-subtitle {
  font-size: 1.125rem;
  color: #6b7280;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon.survey {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
}

.stat-icon.response {
  background: linear-gradient(135deg, #10b981, #047857);
}

.stat-icon.campaign {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.stat-icon.person {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.icon {
  width: 1.5rem;
  height: 1.5rem;
  color: white;
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
}

.stat-label {
  color: #6b7280;
  margin: 0;
  font-size: 0.875rem;
}

.quick-actions {
  margin-top: 3rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 1.5rem 0;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.15);
}

.action-icon {
  width: 3rem;
  height: 3rem;
  color: #3b82f6;
  margin-bottom: 1rem;
}

.action-card h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.action-card p {
  color: #6b7280;
  margin: 0;
  font-size: 0.875rem;
}
</style>