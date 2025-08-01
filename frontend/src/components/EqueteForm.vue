<template>
  <div class="surveys">
    <div class="page-header">
      <h2>Gestion des Enquêtes</h2>
      <button @click="showCreateForm = true" class="primary-btn">
        <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
        Créer une enquête
      </button>
    </div>

    <!-- Formulaire de création/modification -->
    <div v-if="showCreateForm" class="form-modal">
      <div class="form-container">
        <div class="form-header">
          <h3>{{ editingSurvey ? 'Modifier l\'enquête' : 'Nouvelle Enquête' }}</h3>
          <button @click="closeForm" class="close-btn">&times;</button>
        </div>
        
        <form @submit.prevent="saveSurvey" class="survey-form">
          <div class="form-section">
            <h4>Informations générales</h4>
            <div class="form-grid">
              <div class="form-group">
                <label for="titre">Titre de l'enquête *</label>
                <input 
                  id="titre" 
                  v-model="surveyForm.titre" 
                  type="text" 
                  required 
                  class="form-input"
                  placeholder="Entrez le titre de l'enquête"
                />
              </div>
              
              <div class="form-group">
                <label for="campagne">Campagne liée</label>
                <select id="campagne" v-model="surveyForm.campagne" class="form-select">
                  <option value="">Sélectionner une campagne</option>
                  <option value="campagne-1">Satisfaction Client 2024</option>
                  <option value="campagne-2">Étude de marché</option>
                  <option value="campagne-3">Feedback Produit</option>
                </select>
              </div>
              
              <div class="form-group form-group-full">
                <label for="description">Description</label>
                <textarea 
                  id="description" 
                  v-model="surveyForm.description" 
                  class="form-textarea"
                  rows="3"
                  placeholder="Description de l'enquête..."
                ></textarea>
              </div>
            </div>
          </div>

          <div class="form-section">
            <div class="section-header">
              <h4>Questions</h4>
              <button type="button" @click="addQuestion" class="add-question-btn">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
                Ajouter une question
              </button>
            </div>
            
            <div v-if="surveyForm.questions.length === 0" class="no-questions">
              <p>Aucune question ajoutée. Cliquez sur "Ajouter une question" pour commencer.</p>
            </div>
            
            <div v-for="(question, qIndex) in surveyForm.questions" :key="qIndex" class="question-item">
              <div class="question-header">
                <span class="question-number">Question {{ qIndex + 1 }}</span>
                <button type="button" @click="removeQuestion(qIndex)" class="remove-question-btn">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
              
              <div class="question-content">
                <div class="form-group">
                  <label>Texte de la question *</label>
                  <input 
                    v-model="question.texte" 
                    type="text" 
                    required 
                    class="form-input"
                    placeholder="Entrez votre question..."
                  />
                </div>
                
                <div class="form-group">
                  <label>Type de réponse</label>
                  <select v-model="question.type" class="form-select" @change="updateQuestionType(qIndex)">
                    <option value="text">Texte libre</option>
                    <option value="radio">Choix unique</option>
                    <option value="checkbox">Choix multiple</option>
                    <option value="rating">Évaluation (1-5)</option>
                    <option value="yesno">Oui/Non</option>
                  </select>
                </div>
                
                <div v-if="question.type === 'radio' || question.type === 'checkbox'" class="options-section">
                  <label>Options de réponse</label>
                  <div v-for="(option, oIndex) in question.options" :key="oIndex" class="option-item">
                    <input 
                      v-model="question.options[oIndex]" 
                      type="text" 
                      class="form-input"
                      placeholder="Option de réponse..."
                    />
                    <button type="button" @click="removeOption(qIndex, oIndex)" class="remove-option-btn">
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                      </svg>
                    </button>
                  </div>
                  <button type="button" @click="addOption(qIndex)" class="add-option-btn">
                    Ajouter une option
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="closeForm" class="secondary-btn">Annuler</button>
            <button type="submit" class="primary-btn">
              {{ editingSurvey ? 'Modifier' : 'Créer' }} l'enquête
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Barre de recherche -->
    <div class="search-filters">
      <div class="search-bar">
        <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Rechercher des enquêtes..."
          class="search-input"
        />
      </div>
    </div>

    <!-- Tableau des enquêtes -->
    <div class="table-container">
      <table class="surveys-table">
        <thead>
          <tr>
            <th>Titre</th>
            <th>Campagne</th>
            <th>Questions</th>
            <th>Réponses</th>
            <th>Statut</th>
            <th>Date de création</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="survey in filteredSurveys" :key="survey.id" class="table-row">
            <td>
              <div class="survey-title">
                <h4>{{ survey.titre }}</h4>
                <p v-if="survey.description">{{ survey.description }}</p>
              </div>
            </td>
            <td>
              <span v-if="survey.campagne" class="campaign-badge">
                {{ getCampaignName(survey.campagne) }}
              </span>
              <span v-else class="no-campaign">Aucune</span>
            </td>
            <td>{{ survey.questions.length }}</td>
            <td>{{ survey.reponses }}</td>
            <td>
              <span class="status-badge" :class="survey.statut.toLowerCase()">
                {{ survey.statut }}
              </span>
            </td>
            <td>{{ survey.dateCreation }}</td>
            <td>
              <div class="action-buttons">
                <button @click="viewSurvey(survey)" class="action-btn view" title="Voir">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                  </svg>
                </button>
                <button @click="editSurvey(survey)" class="action-btn edit" title="Modifier">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                </button>
                <button @click="deleteSurvey(survey.id)" class="action-btn delete" title="Supprimer">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Question {
  texte: string
  type: string
  options: string[]
}

interface Survey {
  id: number
  titre: string
  description: string
  campagne: string
  questions: Question[]
  reponses: number
  statut: string
  dateCreation: string
}

const showCreateForm = ref(false)
const editingSurvey = ref<Survey | null>(null)
const searchQuery = ref('')

const surveyForm = ref({
  titre: '',
  description: '',
  campagne: '',
  questions: [] as Question[]
})

const surveys = ref<Survey[]>([
  {
    id: 1,
    titre: 'Satisfaction Client 2024',
    description: 'Enquête annuelle de satisfaction des clients',
    campagne: 'campagne-1',
    questions: [
      { texte: 'Comment évaluez-vous notre service ?', type: 'rating', options: [] },
      { texte: 'Recommanderiez-vous nos services ?', type: 'yesno', options: [] }
    ],
    reponses: 245,
    statut: 'Actif',
    dateCreation: '15/03/2024'
  },
  {
    id: 2,
    titre: 'Feedback Produit',
    description: 'Retours sur notre nouveau produit',
    campagne: 'campagne-3',
    questions: [
      { texte: 'Que pensez-vous du design ?', type: 'radio', options: ['Excellent', 'Bon', 'Moyen', 'Mauvais'] },
      { texte: 'Quelles fonctionnalités utilisez-vous le plus ?', type: 'checkbox', options: ['Feature A', 'Feature B', 'Feature C'] }
    ],
    reponses: 89,
    statut: 'Actif',
    dateCreation: '20/03/2024'
  },
  {
    id: 3,
    titre: 'Étude de marché',
    description: 'Analyse des besoins du marché',
    campagne: 'campagne-2',
    questions: [
      { texte: 'Dans quel secteur travaillez-vous ?', type: 'text', options: [] }
    ],
    reponses: 12,
    statut: 'Brouillon',
    dateCreation: '25/03/2024'
  }
])

const filteredSurveys = computed(() => {
  return surveys.value.filter(survey => 
    !searchQuery.value || 
    survey.titre.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    survey.description.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const getCampaignName = (campaignId: string) => {
  const campaigns: Record<string, string> = {
    'campagne-1': 'Satisfaction Client 2024',
    'campagne-2': 'Étude de marché',
    'campagne-3': 'Feedback Produit'
  }
  return campaigns[campaignId] || campaignId
}

const closeForm = () => {
  showCreateForm.value = false
  editingSurvey.value = null
  surveyForm.value = {
    titre: '',
    description: '',
    campagne: '',
    questions: []
  }
}

const addQuestion = () => {
  surveyForm.value.questions.push({
    texte: '',
    type: 'text',
    options: []
  })
}

const removeQuestion = (index: number) => {
  surveyForm.value.questions.splice(index, 1)
}

const updateQuestionType = (qIndex: number) => {
  const question = surveyForm.value.questions[qIndex]
  if (question.type === 'radio' || question.type === 'checkbox') {
    if (question.options.length === 0) {
      question.options = ['Option 1', 'Option 2']
    }
  } else {
    question.options = []
  }
}

const addOption = (qIndex: number) => {
  const question = surveyForm.value.questions[qIndex]
  question.options.push(`Option ${question.options.length + 1}`)
}

const removeOption = (qIndex: number, oIndex: number) => {
  surveyForm.value.questions[qIndex].options.splice(oIndex, 1)
}

const saveSurvey = () => {
  if (editingSurvey.value) {
    // Modifier l'enquête existante
    const index = surveys.value.findIndex(s => s.id === editingSurvey.value!.id)
    if (index !== -1) {
      surveys.value[index] = {
        ...surveys.value[index],
        ...surveyForm.value
      }
    }
  } else {
    // Ajouter une nouvelle enquête
    const newSurvey: Survey = {
      id: Date.now(),
      ...surveyForm.value,
      reponses: 0,
      statut: 'Brouillon',
      dateCreation: new Date().toLocaleDateString('fr-FR')
    }
    surveys.value.push(newSurvey)
  }
  
  closeForm()
}

const viewSurvey = (survey: Survey) => {
  alert(`Affichage de l'enquête: ${survey.titre}`)
}

const editSurvey = (survey: Survey) => {
  editingSurvey.value = survey
  surveyForm.value = {
    titre: survey.titre,
    description: survey.description,
    campagne: survey.campagne,
    questions: JSON.parse(JSON.stringify(survey.questions))
  }
  showCreateForm.value = true
}

const deleteSurvey = (surveyId: number) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer cette enquête ?')) {
    surveys.value = surveys.value.filter(s => s.id !== surveyId)
  }
}
</script>

<style scoped>
.surveys {
  max-width: 1200px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.primary-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.primary-btn:hover {
  background-color: #2563eb;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

.form-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 1rem;
}

.form-container {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.form-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0.25rem;
  border-radius: 4px;
}

.close-btn:hover {
  background-color: #f3f4f6;
}

.survey-form {
  padding: 1.5rem;
}

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.form-section:last-of-type {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.form-section h4 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.add-question-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-question-btn:hover {
  background-color: #059669;
}

.add-question-btn svg {
  width: 16px;
  height: 16px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.form-group-full {
  grid-column: 1 / -1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #374151;
}

.form-input, .form-select, .form-textarea {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.no-questions {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
  background-color: #f9fafb;
  border-radius: 8px;
  border: 2px dashed #d1d5db;
}

.question-item {
  background-color: #f9fafb;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  margin-bottom: 1rem;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-number {
  font-weight: 600;
  color: #3b82f6;
}

.remove-question-btn {
  padding: 0.25rem;
  background-color: #fee2e2;
  color: #dc2626;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.remove-question-btn:hover {
  background-color: #fecaca;
}

.remove-question-btn svg {
  width: 16px;
  height: 16px;
}

.question-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1rem;
  align-items: start;
}

.options-section {
  grid-column: 1 / -1;
  margin-top: 1rem;
}

.options-section label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.option-item {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  align-items: center;
}

.option-item input {
  flex: 1;
}

.remove-option-btn {
  padding: 0.5rem;
  background-color: #fee2e2;
  color: #dc2626;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  flex-shrink: 0;
}

.remove-option-btn svg {
  width: 14px;
  height: 14px;
}

.add-option-btn {
  padding: 0.5rem 1rem;
  background-color: #e0e7ff;
  color: #4338ca;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-option-btn:hover {
  background-color: #c7d2fe;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.secondary-btn {
  padding: 0.75rem 1.5rem;
  background-color: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.secondary-btn:hover {
  background-color: #e5e7eb;
}

.search-filters {
  margin-bottom: 2rem;
}

.search-bar {
  position: relative;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #6b7280;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.table-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.surveys-table {
  width: 100%;
  border-collapse: collapse;
}

.surveys-table th {
  background-color: #f9fafb;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
}

.table-row {
  transition: background-color 0.2s;
}

.table-row:hover {
  background-color: #f9fafb;
}

.surveys-table td {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
  vertical-align: middle;
}

.survey-title h4 {
  margin: 0 0 0.25rem 0;
  font-weight: 600;
  color: #1f2937;
}

.survey-title p {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.campaign-badge {
  padding: 0.25rem 0.75rem;
  background-color: #dbeafe;
  color: #3b82f6;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
}

.no-campaign {
  color: #6b7280;
  font-style: italic;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.actif {
  background-color: #d1fae5;
  color: #059669;
}

.status-badge.brouillon {
  background-color: #fef3c7;
  color: #d97706;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.action-btn.view {
  background-color: #e0e7ff;
  color: #4338ca;
}

.action-btn.view:hover {
  background-color: #c7d2fe;
}

.action-btn.edit {
  background-color: #dbeafe;
  color: #3b82f6;
}

.action-btn.edit:hover {
  background-color: #bfdbfe;
}

.action-btn.delete {
  background-color: #fee2e2;
  color: #dc2626;
}

.action-btn.delete:hover {
  background-color: #fecaca;
}

@media (max-width: 767px) {
  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .question-content {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .surveys-table {
    min-width: 900px;
  }
}
</style>