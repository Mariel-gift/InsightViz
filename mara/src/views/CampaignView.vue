<template>
  <div class="campaign-view">
    <div class="page-header">
      <h1 class="page-title">Gestion des Campagnes</h1>
      <p class="page-subtitle">Organisez et suivez vos campagnes de communication</p>
    </div>

    <CrudTable
      title="Campagne"
      :columns="columns"
      :fields="fields"
      :data="campaigns"
      @add="addCampaign"
      @edit="editCampaign"
      @delete="deleteCampaign"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CrudTable from '../components/CrudTable.vue'

const columns = [
  { key: 'name', label: 'Nom' },
  { key: 'type', label: 'Type' },
  { key: 'status', label: 'Statut' },
  { key: 'startDate', label: 'Date de début' },
  { key: 'endDate', label: 'Date de fin' },
  { key: 'reach', label: 'Portée' }
]

const fields = [
  { key: 'name', label: 'Nom de la campagne', required: true },
  { key: 'type', label: 'Type', required: true },
  { key: 'status', label: 'Statut', required: true },
  { key: 'startDate', label: 'Date de début', type: 'date', required: true },
  { key: 'endDate', label: 'Date de fin', type: 'date', required: true },
  { key: 'budget', label: 'Budget', type: 'number', required: false }
]

const campaigns = ref([
  {
    id: 1,
    name: 'Campagne Printemps 2025',
    type: 'Email Marketing',
    status: 'En cours',
    startDate: '2025-01-15',
    endDate: '2025-04-15',
    reach: '2,500 contacts',
    budget: 5000
  },
  {
    id: 2,
    name: 'Lancement Produit X',
    type: 'Multi-canal',
    status: 'Planifiée',
    startDate: '2025-02-01',
    endDate: '2025-03-01',
    reach: '10,000 contacts',
    budget: 15000
  },
  {
    id: 3,
    name: 'Satisfaction Client Q4',
    type: 'Enquête',
    status: 'Terminée',
    startDate: '2024-10-01',
    endDate: '2024-12-31',
    reach: '1,200 contacts',
    budget: 2000
  },
  {
    id: 4,
    name: 'Newsletter Janvier',
    type: 'Newsletter',
    status: 'En cours',
    startDate: '2025-01-01',
    endDate: '2025-01-31',
    reach: '5,000 contacts',
    budget: 800
  }
])

const addCampaign = (newCampaign: any) => {
  campaigns.value.push({
    ...newCampaign,
    reach: '0 contacts'
  })
}

const editCampaign = (updatedCampaign: any) => {
  const index = campaigns.value.findIndex(c => c.id === updatedCampaign.id)
  if (index !== -1) {
    campaigns.value[index] = { ...campaigns.value[index], ...updatedCampaign }
  }
}

const deleteCampaign = (id: number) => {
  campaigns.value = campaigns.value.filter(c => c.id !== id)
}
</script>

<style scoped>
.campaign-view {
  padding: 2rem;
}

.page-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.page-subtitle {
  color: #6b7280;
  margin: 0;
}
</style>