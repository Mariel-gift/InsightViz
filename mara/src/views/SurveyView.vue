<template>
  <div class="survey-view">
    <div class="page-header">
      <h1 class="page-title">Gestion des Enquêtes</h1>
      <p class="page-subtitle">Créez et gérez vos enquêtes de satisfaction</p>
    </div>

    <CrudTable
      title="Enquête"
      :columns="columns"
      :fields="fields"
      :data="surveys"
      @add="addSurvey"
      @edit="editSurvey"
      @delete="deleteSurvey"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CrudTable from '../components/CrudTable.vue'

const columns = [
  { key: 'title', label: 'Titre' },
  { key: 'description', label: 'Description' },
  { key: 'status', label: 'Statut' },
  { key: 'createdDate', label: 'Date de création' },
  { key: 'responses', label: 'Réponses' }
]

const fields = [
  { key: 'title', label: 'Titre', required: true },
  { key: 'description', label: 'Description', required: true },
  { key: 'status', label: 'Statut', required: true },
  { key: 'targetAudience', label: 'Public cible', required: true }
]

const surveys = ref([
  {
    id: 1,
    title: 'Satisfaction client Q1 2025',
    description: 'Enquête de satisfaction trimestrielle',
    status: 'Active',
    createdDate: '2025-01-15',
    responses: 45,
    targetAudience: 'Clients Premium'
  },
  {
    id: 2,
    title: 'Évaluation produit X',
    description: 'Retours sur le nouveau produit lancé',
    status: 'Brouillon',
    createdDate: '2025-01-12',
    responses: 0,
    targetAudience: 'Beta testeurs'
  },
  {
    id: 3,
    title: 'Service après-vente',
    description: 'Qualité du support client',
    status: 'Terminée',
    createdDate: '2024-12-20',
    responses: 128,
    targetAudience: 'Tous clients'
  }
])

const addSurvey = (newSurvey: any) => {
  surveys.value.push({
    ...newSurvey,
    createdDate: new Date().toISOString().split('T')[0],
    responses: 0
  })
}

const editSurvey = (updatedSurvey: any) => {
  const index = surveys.value.findIndex(s => s.id === updatedSurvey.id)
  if (index !== -1) {
    surveys.value[index] = { ...surveys.value[index], ...updatedSurvey }
  }
}

const deleteSurvey = (id: number) => {
  surveys.value = surveys.value.filter(s => s.id !== id)
}
</script>

<style scoped>
.survey-view {
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