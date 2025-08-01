<template>
  <div class="person-view">
    <div class="page-header">
      <h1 class="page-title">Gestion des Personnes</h1>
      <p class="page-subtitle">Administrez votre base de contacts et utilisateurs</p>
    </div>

    <CrudTable
      title="Personne"
      :columns="columns"
      :fields="fields"
      :data="persons"
      :show-search="true"
      @add="addPerson"
      @edit="editPerson"
      @delete="deletePerson"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CrudTable from '../components/CrudTable.vue'

const columns = [
  { key: 'firstName', label: 'Prénom' },
  { key: 'lastName', label: 'Nom' },
  { key: 'email', label: 'Email' },
  { key: 'phone', label: 'Téléphone' },
  { key: 'company', label: 'Entreprise' },
  { key: 'role', label: 'Rôle' }
]

const fields = [
  { key: 'firstName', label: 'Prénom', required: true },
  { key: 'lastName', label: 'Nom', required: true },
  { key: 'email', label: 'Email', type: 'email', required: true },
  { key: 'phone', label: 'Téléphone', type: 'tel', required: false },
  { key: 'company', label: 'Entreprise', required: false },
  { key: 'role', label: 'Rôle', required: false }
]

const persons = ref([
  {
    id: 1,
    firstName: 'Jean',
    lastName: 'Dupont',
    email: 'jean.dupont@example.com',
    phone: '+33 1 23 45 67 89',
    company: 'TechCorp',
    role: 'Développeur'
  },
  {
    id: 2,
    firstName: 'Marie',
    lastName: 'Martin',
    email: 'marie.martin@example.com',
    phone: '+33 1 23 45 67 90',
    company: 'DesignStudio',
    role: 'Designer'
  },
  {
    id: 3,
    firstName: 'Pierre',
    lastName: 'Durand',
    email: 'pierre.durand@example.com',
    phone: '+33 1 23 45 67 91',
    company: 'ConsultingFirm',
    role: 'Consultant'
  },
  {
    id: 4,
    firstName: 'Sophie',
    lastName: 'Laurent',
    email: 'sophie.laurent@example.com',
    phone: '+33 1 23 45 67 92',
    company: 'MarketingAgency',
    role: 'Chef de projet'
  },
  {
    id: 5,
    firstName: 'Thomas',
    lastName: 'Moreau',
    email: 'thomas.moreau@example.com',
    phone: '+33 1 23 45 67 93',
    company: 'StartupInc',
    role: 'CTO'
  },
  {
    id: 6,
    firstName: 'Emma',
    lastName: 'Bernard',
    email: 'emma.bernard@example.com',
    phone: '+33 1 23 45 67 94',
    company: 'FinanceGroup',
    role: 'Analyste'
  }
])

const addPerson = (newPerson: any) => {
  persons.value.push(newPerson)
}

const editPerson = (updatedPerson: any) => {
  const index = persons.value.findIndex(p => p.id === updatedPerson.id)
  if (index !== -1) {
    persons.value[index] = { ...persons.value[index], ...updatedPerson }
  }
}

const deletePerson = (id: number) => {
  persons.value = persons.value.filter(p => p.id !== id)
}
</script>

<style scoped>
.person-view {
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