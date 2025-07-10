<template>
  <div class="dashboard-container">
    <!-- Sidebar -->
    <aside class="sidebar">
      <h2 class="sidebar-title">InsightViz</h2>
      <ul class="sidebar-menu">
        <li><a href="#" @click.prevent="sectionActive = 'accueil'">Accueil</a></li>
        <li><a href="#" @click.prevent="sectionActive = 'stats'">Statistiques</a></li>
        <li><a href="#" @click.prevent="sectionActive = 'utilisateurForm'">Utilisateurs</a></li>
      </ul>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
     <header class="dashboard-header">
  <h1>{{ titrePrincipal }}</h1>
  <h2 class="welcome-text" v-if="sectionActive === 'accueil' || sectionActive === 'stats'">Bienvenue, Mariel</h2>
</header>


      <!-- Section Accueil ou Statistiques -->
      <section v-if="sectionActive === 'accueil' || sectionActive === 'stats'">
        <!-- Filtres de date -->
        <section class="filters">
          <label>
            Début :
            <input type="date" v-model="dateDebut" />
          </label>
          <label>
            Fin :
            <input type="date" v-model="dateFin" />
          </label>
          <button @click="chargerStats">Filtrer</button>
        </section>

        <!-- Cartes de statistiques -->
        <section class="stats-grid">
          <div class="stat-card" v-for="(value, key) in stats" :key="key">
            <h3>{{ formatKey(key) }}</h3>
            <p>{{ value }}</p>
          </div>
        </section>

        <!-- Graphique -->
        <section class="chart-section">
          <h2>Enquêtes par mois</h2>
          <Bar :data="chartData" :options="chartOptions" />
        </section>
      </section>

      <!-- Formulaire utilisateur dynamique -->
      <section v-if="sectionActive === 'utilisateurForm'">
        <UserForm @soumission-success="handleUserAdded" />
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Bar } from 'vue-chartjs'
import UserForm from './UserForm.vue'
import { computed } from 'vue'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const sectionActive = ref('accueil')
const dateDebut = ref('')
const dateFin = ref('')

const stats = ref({
  enquêtes: 0,
  campagnes: 0,
  réponses: 0,
  utilisateurs: 0
})

const utilisateurs = ref([])

const handleUserAdded = () => {
  sectionActive.value = 'accueil'
  chargerUtilisateurs()
}

const chargerStats = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/api/dashboard/stats', {
      params: {
        start: dateDebut.value,
        end: dateFin.value
      }
    })
    stats.value = res.data
  } catch (err) {
    console.error('Erreur chargement stats :', err)
  }
}

const chargerUtilisateurs = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/api/utilisateurs')
    utilisateurs.value = res.data
  } catch (err) {
    console.error('Erreur chargement utilisateurs :', err)
  }
}

onMounted(() => {
  chargerStats()
  chargerUtilisateurs()
})

const chartData = {
  labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov', 'Déc'],
  datasets: [
    {
      label: 'Enquêtes',
      data: [120, 180, 250, 230, 310, 400, 390, 360, 420, 480, 500, 530],
      backgroundColor: '#6a11cb'
    }
  ]
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
}

const formatKey = (key) => {
  const map = {
    "enquêtes": "Enquêtes",
    "campagnes": "Campagnes marketing",
    "réponses": "Réponses reçues",
    "utilisateurs": "Utilisateurs"
  }
  return map[key] || key
}

const titrePrincipal = computed(() => {
  switch (sectionActive.value) {
    case 'accueil':
    case 'stats':
      return 'Tableau de bord'
    case 'utilisateurForm':
      return ' Utilisateur'
    default:
      return 'InsightViz'
  }
})
</script>

<style scoped>
.dashboard-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  overflow: hidden;
  font-family: 'Segoe UI', sans-serif;
  background-color: #f0f4f8;
}

.sidebar {
  width: 220px;
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  color: white;
  padding: 1.5rem;
}

.sidebar-title {
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 2rem;
  text-align: center;
}

.sidebar-menu {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.sidebar-menu a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  display: block;
  padding: 0.4rem 0.6rem;
  border-radius: 8px;
  text-align: center;
  transition: background 0.3s ease;
}

.sidebar-menu a:hover {
  background-color: rgba(255, 255, 255, 0.15);
}

.main-content {
  flex: 1;
  height: 100vh;
  overflow-y: auto;
  background-color: #ffffff;
  padding: 2rem;
}

.dashboard-header h1 {
  margin: 0;
  font-size: 2.2rem;
  color: #2c3e50;
}

.welcome-text {
  margin-top: 0.5rem;
  font-size: 1.3rem;
  color: #555;
}

.filters {
  display: flex;
  gap: 1rem;
  margin: 1.5rem 0;
  flex-wrap: wrap;
}

.filters label {
  font-weight: 500;
  color: #2c3e50;
}

.filters input[type="date"] {
  padding: 0.4rem;
  margin-left: 0.5rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.filters button {
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  color: white;
  border: none;
  padding: 0.5rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: transform 0.2s ease;
}

.filters button:hover {
  transform: scale(1.05);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background-color: #fefefe;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.stat-card h3 {
  margin: 0;
  font-size: 1rem;
  color: #34495e;
}

.stat-card p {
  font-size: 1.6rem;
  font-weight: bold;
  margin-top: 0.5rem;
  color: #2c3e50;
}

.chart-section {
  margin-top: 2rem;
  background: #ffffff;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  height: 300px;
}
</style>
