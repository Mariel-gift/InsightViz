<template>
  <div class="response-view">
    <div class="page-header">
      <h1 class="page-title">Gestion des Réponses</h1>
      <p class="page-subtitle">Consultez et analysez les réponses aux enquêtes</p>
    </div>

    <CrudTable
      title="Réponse"
      :columns="columns"
      :fields="fields"
      :data="responses"
      @add="addResponse"
      @edit="editResponse"
      @delete="deleteResponse"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CrudTable from '../components/CrudTable.vue'

const columns = [
  { key: 'surveyTitle', label: 'Enquête' },
  { key: 'respondent', label: 'Répondant' },
  { key: 'rating', label: 'Note' },
  { key: 'comment', label: 'Commentaire' },
  { key: 'responseDate', label: 'Date de réponse' }
]

const fields = [
  { key: 'surveyTitle', label: 'Enquête', required: true },
  { key: 'respondent', label: 'Répondant', required: true },
  { key: 'rating', label: 'Note', type: 'number', required: true },
  { key: 'comment', label: 'Commentaire', required: false }
]

const responses = ref([
  {
    id: 1,
    surveyTitle: 'Satisfaction client Q1 2025',
    respondent: 'Jean Dupont',
    rating: 8,
    comment: 'Service excellent, très satisfait',
    responseDate: '2025-01-18'
  },
  {
    id: 2,
    surveyTitle: 'Satisfaction client Q1 2025',
    respondent: 'Marie Martin',
    rating: 7,
    comment: 'Bon service dans l\'ensemble',
    responseDate: '2025-01-17'
  },
  {
    id: 3,
    surveyTitle: 'Service après-vente',
    respondent: 'Pierre Durand',
    rating: 9,
    comment: 'Support réactif et compétent',
    responseDate: '2025-01-16'
  },
  {
    id: 4,
    surveyTitle: 'Évaluation produit X',
    respondent: 'Sophie Laurent',
    rating: 6,
    comment: 'Produit correct mais peut mieux faire',
    responseDate: '2025-01-15'
  }
])

const addResponse = (newResponse: any) => {
  responses.value.push({
    ...newResponse,
    responseDate: new Date().toISOString().split('T')[0]
  })
}

const editResponse = (updatedResponse: any) => {
  const index = responses.value.findIndex(r => r.id === updatedResponse.id)
  if (index !== -1) {
    responses.value[index] = { ...responses.value[index], ...updatedResponse }
  }
}

const deleteResponse = (id: number) => {
  responses.value = responses.value.filter(r => r.id !== id)
}
</script>

<style scoped>
.response-view {
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