<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h2>Tableau de bord</h2>
      <p>Vue d'ensemble de vos données InsightViz</p>
    </div>

    <!-- Compteurs de résumé -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon surveys">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
          </svg>
        </div>
        <div class="stat-content">
          <h3>{{ stats.surveys }}</h3>
          <p>Enquêtes</p>
          <span class="stat-change positive">+12% ce mois</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon responses">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <h3>{{ stats.responses }}</h3>
          <p>Réponses</p>
          <span class="stat-change positive">+28% ce mois</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon campaigns">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <h3>{{ stats.campaigns }}</h3>
          <p>Campagnes</p>
          <span class="stat-change neutral">Stable</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon users">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <h3>{{ stats.users }}</h3>
          <p>Utilisateurs</p>
          <span class="stat-change positive">+5% ce mois</span>
        </div>
      </div>
    </div>

    <!-- Graphique de données -->
    <div class="chart-container">
      <div class="chart-header">
        <h3>Évolution des réponses</h3>
        <div class="chart-period">
          <button 
            v-for="period in chartPeriods" 
            :key="period.value"
            @click="selectedPeriod = period.value"
            class="period-btn"
            :class="{ active: selectedPeriod === period.value }"
          >
            {{ period.label }}
          </button>
        </div>
      </div>
      <div class="chart">
        <div class="chart-bars">
          <div 
            v-for="(data, index) in chartData" 
            :key="index"
            class="chart-bar"
            :style="{ height: `${(data.value / maxValue) * 100}%` }"
          >
            <div class="bar-value">{{ data.value }}</div>
          </div>
        </div>
        <div class="chart-labels">
          <div v-for="(data, index) in chartData" :key="index" class="chart-label">
            {{ data.label }}
          </div>
        </div>
      </div>
    </div>

    <!-- Activité récente -->
    <div class="recent-activity">
      <h3>Activité récente</h3>
      <div class="activity-list">
        <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
          <div class="activity-icon" :class="activity.type">
            <svg v-if="activity.type === 'survey'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
            </svg>
            <svg v-else-if="activity.type === 'response'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
            <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
          </div>
          <div class="activity-content">
            <p class="activity-text">{{ activity.text }}</p>
            <span class="activity-time">{{ activity.time }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const stats = ref({
  surveys: 24,
  responses: 1847,
  campaigns: 8,
  users: 156
})

const selectedPeriod = ref('7j')
const chartPeriods = [
  { label: '7 jours', value: '7j' },
  { label: '30 jours', value: '30j' },
  { label: '3 mois', value: '3m' }
]

const chartData = ref([
  { label: 'Lun', value: 120 },
  { label: 'Mar', value: 190 },
  { label: 'Mer', value: 170 },
  { label: 'Jeu', value: 240 },
  { label: 'Ven', value: 310 },
  { label: 'Sam', value: 180 },
  { label: 'Dim', value: 95 }
])

const maxValue = computed(() => Math.max(...chartData.value.map(d => d.value)))

const recentActivities = ref([
  {
    id: 1,
    type: 'survey',
    text: 'Nouvelle enquête "Satisfaction Client 2024" créée par Marie Dubois',
    time: 'Il y a 2 heures'
  },
  {
    id: 2,
    type: 'response',
    text: '15 nouvelles réponses reçues pour l\'enquête "Feedback Produit"',
    time: 'Il y a 3 heures'
  },
  {
    id: 3,
    type: 'user',
    text: 'Nouvel utilisateur Pierre Martin ajouté au système',
    time: 'Il y a 5 heures'
  },
  {
    id: 4,
    type: 'survey',
    text: 'Enquête "Étude de marché" modifiée par Sophie Laurent',
    time: 'Il y a 1 jour'
  }
])
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.dashboard-header p {
  color: #6b7280;
  font-size: 1.1rem;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 28px;
  height: 28px;
}

.stat-icon.surveys {
  background-color: #dbeafe;
  color: #3b82f6;
}

.stat-icon.responses {
  background-color: #d1fae5;
  color: #10b981;
}

.stat-icon.campaigns {
  background-color: #fef3c7;
  color: #f59e0b;
}

.stat-icon.users {
  background-color: #ede9fe;
  color: #8b5cf6;
}

.stat-content h3 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
}

.stat-content p {
  color: #6b7280;
  font-weight: 500;
  margin: 0 0 0.5rem 0;
}

.stat-change {
  font-size: 0.875rem;
  font-weight: 500;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change.neutral {
  color: #6b7280;
}

.chart-container {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.chart-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.chart-period {
  display: flex;
  gap: 0.5rem;
}

.period-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.period-btn:hover {
  border-color: #3b82f6;
}

.period-btn.active {
  background-color: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.chart {
  height: 300px;
  display: flex;
  flex-direction: column;
}

.chart-bars {
  flex: 1;
  display: flex;
  align-items: end;
  gap: 1rem;
  padding: 1rem 0;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(to top, #3b82f6, #60a5fa);
  border-radius: 4px 4px 0 0;
  min-height: 20px;
  position: relative;
  transition: all 0.3s ease;
}

.chart-bar:hover {
  background: linear-gradient(to top, #2563eb, #3b82f6);
}

.bar-value {
  position: absolute;
  top: -1.5rem;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.chart-labels {
  display: flex;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.chart-label {
  flex: 1;
  text-align: center;
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.recent-activity {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.recent-activity h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 1.5rem 0;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.activity-item:hover {
  background-color: #f9fafb;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-icon svg {
  width: 20px;
  height: 20px;
}

.activity-icon.survey {
  background-color: #dbeafe;
  color: #3b82f6;
}

.activity-icon.response {
  background-color: #d1fae5;
  color: #10b981;
}

.activity-icon.user {
  background-color: #ede9fe;
  color: #8b5cf6;
}

.activity-content {
  flex: 1;
}

.activity-text {
  margin: 0 0 0.25rem 0;
  color: #1f2937;
  font-weight: 500;
}

.activity-time {
  color: #6b7280;
  font-size: 0.875rem;
}

@media (max-width: 767px) {
  .chart-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-bars {
    gap: 0.5rem;
  }
  
  .chart-labels {
    gap: 0.5rem;
  }
}
</style>