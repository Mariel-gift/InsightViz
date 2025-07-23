<template>
  <div class="admin-home">
    <!-- KPI alignés horizontalement -->
    <div class="kpi-row">
      <div class="kpi-card" v-for="k in kpis" :key="k.label">
        <h3>{{ k.value }}</h3>
        <div class="icon-title">
          <span class="icon" v-html="k.icon"></span>
          <p>{{ k.label }}</p>
        </div>
      </div>
    </div>

    <!-- Graphique -->
    <div class="chart-wrapper">
      <canvas id="enqueteChart"></canvas>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import axios from 'axios'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

const kpis = reactive([
  {
    label: 'Enquêtes',
    value: 0,
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="#6a11cb" viewBox="0 0 24 24">
             <path d="M3 4v16h18V4H3zm16 14H5V6h14v12z"/><path d="M7 8h10v2H7zm0 4h6v2H7z"/>
           </svg>`
  },
  {
    label: 'Réponses',
    value: 0,
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="#6a11cb" viewBox="0 0 24 24">
             <path d="M21 6h-2V4H5v2H3v14h18V6zM5 8h14v10H5V8z"/>
           </svg>`
  },
  {
    label: 'Campagnes',
    value: 0,
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="#6a11cb" viewBox="0 0 24 24">
             <path d="M21 4v13h-4v3l-5-3h-8V4h17zm-2 2H5v9h5l4 2.5V15h5V6z"/>
           </svg>`
  },
  {
    label: 'Utilisateurs',
    value: 0,
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="#6a11cb" viewBox="0 0 24 24">
             <path d="M12 12c2.7 0 5-2.3 5-5s-2.3-5-5-5-5 2.3-5 5 2.3 5 5 5zm0 2c-3.3 0-10 1.7-10 5v3h20v-3c0-3.3-6.7-5-10-5z"/>
           </svg>`
  }
])

const months = []
const enquetesMonthly = []

let chart
const draw = () => {
  if (chart) chart.destroy()
  chart = new Chart(document.getElementById('enqueteChart'), {
    type: 'line',
    data: {
      labels: months,
      datasets: [{
        label: 'Enquêtes/mois',
        data: enquetesMonthly,
        tension: 0.35,
        borderColor: '#6a11cb',
        backgroundColor: 'rgba(106,17,203,0.1)',
        pointBackgroundColor: '#6a11cb'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  })
}

onMounted(async () => {
  try {
    const { data } = await axios.get('/api/backoffice/stats')
    kpis[0].value = data.enquetes
    kpis[1].value = data.reponses
    kpis[2].value = data.campagnes
    kpis[3].value = data.utilisateurs
    months.push(...data.months)
    enquetesMonthly.push(...data.enquetesMonthly)
  } catch {
    Object.assign(kpis[0], { value: 42 })
    Object.assign(kpis[1], { value: 180 })
    Object.assign(kpis[2], { value: 6 })
    Object.assign(kpis[3], { value: 85 })
    months.push('Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc')
    enquetesMonthly.push(2, 4, 3, 5, 6, 4, 7, 5, 3, 4, 2, 7)
  }
  draw()
})
</script>

<style scoped>
.admin-home {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.kpi-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  flex-wrap: nowrap;
}

.kpi-card {
  flex: 1;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .06);
  padding: 1.5rem;
  text-align: center;
}

.kpi-card h3 {
  margin: 0;
  font-size: 2.4rem;
  color: #6a11cb;
}

.icon-title {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 0.5rem;
  gap: 0.4rem;
}

.kpi-card p {
  margin: 0;
  font-weight: 600;
  color: #555;
}

.chart-wrapper {
  flex: 1;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .06);
  padding: 1rem;
  min-height: 300px;
}

.chart-wrapper canvas {
  width: 100%;
  height: 100%;
}
</style>
