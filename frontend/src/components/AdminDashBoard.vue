<template>
  <div class="admin-layout">
    <!-- ===== SIDEBAR ===== -->
    <aside class="sidebar">
      <h2 class="logo">InsightViz</h2>

      <button class="sidebar-btn" @click="router.push({ name: 'Dashboard' })">
        Retour site public
      </button>

      <div class="dropdown">
        <label for="paramSelect">Paramètre</label>
        <select id="paramSelect" v-model="selectedParam" @change="handleParam">
          <option disabled value="">— Choisir —</option>
          <option value="user">Utilisateur</option>
          <option value="enquete">Enquête</option>
          <option value="reponse">Réponse</option>
          <option value="campagne">Campagne</option>
          <option value="personne">Personne</option>
        </select>
      </div>
    </aside>

    <!-- ===== CONTENU DASHBOARD ===== -->
    <main class="content">
      <h1 class="dash-title">Tableau de bord admin</h1>

      <!-- KPI en ligne -->
      <div class="kpi-row">
        <div class="kpi-card">
          <h3>{{ stats.enquetes }}</h3>
          <p>Enquêtes</p>
        </div>
        <div class="kpi-card">
          <h3>{{ stats.reponses }}</h3>
          <p>Réponses</p>
        </div>
        <div class="kpi-card">
          <h3>{{ stats.campagnes }}</h3>
          <p>Campagnes</p>
        </div>
        <div class="kpi-card">
          <h3>{{ stats.utilisateurs }}</h3>
          <p>Utilisateurs</p>
        </div>
      </div>

      <!-- Graphique -->
      <div class="chart-wrapper">
        <canvas id="enqueteChart"></canvas>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../axios'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

/* ===== Navigation ===== */
const router = useRouter()
const selectedParam = ref('')
const handleParam = () => {
  const map = { user:'UserForm', enquete:'EqueteForm', reponse:'ReponseForm', campagne:'CampagneForm',personne:'PersonneForm' }
  if (selectedParam.value && map[selectedParam.value]) {
    router.push({ name: map[selectedParam.value] })
    selectedParam.value = ''
  }
}

/* ===== Stats réactives ===== */
const stats = reactive({
  enquetes: 0, reponses: 0, campagnes: 0, utilisateurs: 0,
  months: [], enquetesMonthly: []
})

let chartInstance
const renderChart = () => {
  if (chartInstance) chartInstance.destroy()
  const ctx = document.getElementById('enqueteChart').getContext('2d')
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: stats.months,
      datasets: [{ label:'Enquêtes/mois', data:stats.enquetesMonthly, fill:false, tension:.35 }]
    },
    options: { responsive:true, maintainAspectRatio:false }
  })
}

const fetchStats = async () => {
  try {
    const { data } = await axios.get('/api/backoffice/stats')
    Object.assign(stats, data)
  } catch {
    /* Données factices */
    Object.assign(stats, {
      enquetes: 42, reponses: 180, campagnes: 6, utilisateurs: 85,
      months:['Jan','Fév','Mar','Avr','Mai','Juin','Juil','Aoû','Sep','Oct','Nov','Déc'],
      enquetesMonthly:[2,4,3,5,6,4,7,5,3,4,2,7]
    })
  }
  renderChart()
}

onMounted(fetchStats)
</script>

<style scoped>
/* ===== Layout plein écran ===== */
.admin-layout{display:flex;height:100vh;overflow:hidden}

/* ===== Sidebar ===== */
.sidebar{
  position:fixed;top:0;left:0;width:260px;height:100vh;
  padding:2rem 1rem;display:flex;flex-direction:column;gap:1.5rem;
  background:linear-gradient(135deg,#372d67 0%,#6a11cb 60%,#2575fc 100%);
  color:#fff;box-shadow:2px 0 10px rgba(0,0,0,.15)
}
.logo{font-size:1.5rem;font-weight:700;text-align:center;margin-bottom:1rem}
.sidebar-btn{
  background:#fff;color:#6a11cb;border:none;padding:.7rem 1rem;border-radius:8px;font-weight:600;cursor:pointer
}
.sidebar-btn:hover{opacity:.9}
.dropdown label{display:block;margin-bottom:.35rem;font-size:.95rem}
.dropdown select{width:100%;padding:.55rem;border-radius:6px;border:none;background:rgba(255,255,255,.15);color:#370592}

/* ===== Contenu ===== */
.content{
  margin-left:260px;height:100vh;overflow-y:auto;background:#f9f9fe;
  padding:2rem 1.5rem;display:flex;flex-direction:column
}
.dash-title{margin-bottom:1.5rem;color:#2c3e50}

/* ===== KPI ROW (horizontale) ===== */
.kpi-row{
  display:flex;gap:1.5rem;margin-bottom:2rem;
  flex-wrap:nowrap; /* force une seule ligne */
}
.kpi-card{
  flex:1; /* chaque carte prend la même largeur */
  background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.06);
  padding:1.5rem;text-align:center
}
.kpi-card h3{margin:0;font-size:2.4rem;color:#6a11cb}
.kpi-card p{margin:0;margin-top:.35rem;font-weight:600;color:#555}

/* ===== Graphique ===== */
.chart-wrapper{
  flex:1; /* prend tout l'espace restant pour un vrai plein écran */
  background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.06);
  padding:1rem;min-height:300px
}
.chart-wrapper canvas{width:100%;height:100%}
</style>
