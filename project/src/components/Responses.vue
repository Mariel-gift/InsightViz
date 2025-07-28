<template>
  <div class="responses">
    <div class="page-header">
      <h2>Réponses aux Enquêtes</h2>
      <div class="header-actions">
        <select v-model="selectedSurvey" class="survey-select">
          <option value="">Toutes les enquêtes</option>
          <option v-for="survey in availableSurveys" :key="survey.id" :value="survey.id">
            {{ survey.title }}
          </option>
        </select>
      </div>
    </div>

    <!-- Interface de soumission de réponse -->
    <div class="response-form-section">
      <h3>Soumettre une nouvelle réponse</h3>
      
      <div class="survey-selector">
        <label for="survey-to-answer">Choisir une enquête *</label>
        <select id="survey-to-answer" v-model="surveyToAnswer" class="form-select" @change="loadSurveyQuestions">
          <option value="">Sélectionner une enquête</option>
          <option v-for="survey in availableSurveys" :key="survey.id" :value="survey.id">
            {{ survey.title }}
          </option>
        </select>
      </div>

      <div v-if="currentSurveyQuestions.length > 0" class="response-form">
        <div class="survey-info">
          <h4>{{ getCurrentSurvey()?.title }}</h4>
          <p v-if="getCurrentSurvey()?.description">{{ getCurrentSurvey()?.description }}</p>
        </div>

        <form @submit.prevent="submitResponse" class="answer-form">
          <div v-for="(question, index) in currentSurveyQuestions" :key="index" class="question-block">
            <div class="question-header">
              <span class="question-number">{{ index + 1 }}.</span>
              <label class="question-text">{{ question.text }}</label>
              <span v-if="question.required" class="required">*</span>
            </div>

            <div class="answer-input">
              <!-- Texte libre -->
              <textarea 
                v-if="question.type === 'text'"
                v-model="responseForm[index]"
                class="form-textarea"
                placeholder="Votre réponse..."
                :required="question.required"
              ></textarea>

              <!-- Choix unique -->
              <div v-else-if="question.type === 'radio'" class="radio-group">
                <label v-for="option in question.options" :key="option" class="radio-option">
                  <input 
                    type="radio" 
                    :name="`question_${index}`"
                    :value="option"
                    v-model="responseForm[index]"
                    :required="question.required"
                  />
                  <span>{{ option }}</span>
                </label>
              </div>

              <!-- Choix multiple -->
              <div v-else-if="question.type === 'checkbox'" class="checkbox-group">
                <label v-for="option in question.options" :key="option" class="checkbox-option">
                  <input 
                    type="checkbox" 
                    :value="option"
                    @change="updateCheckboxResponse(index, option, $event)"
                  />
                  <span>{{ option }}</span>
                </label>
              </div>

              <!-- Évaluation 1-5 -->
              <div v-else-if="question.type === 'rating'" class="rating-group">
                <div class="rating-scale">
                  <label v-for="rating in 5" :key="rating" class="rating-option">
                    <input 
                      type="radio" 
                      :name="`question_${index}`"
                      :value="rating"
                      v-model="responseForm[index]"
                      :required="question.required"
                    />
                    <span class="rating-number">{{ rating }}</span>
                  </label>
                </div>
                <div class="rating-labels">
                  <span>Très mauvais</span>
                  <span>Excellent</span>
                </div>
              </div>

              <!-- Oui/Non -->
              <div v-else-if="question.type === 'yesno'" class="yesno-group">
                <label class="radio-option">
                  <input 
                    type="radio" 
                    :name="`question_${index}`"
                    value="Oui"
                    v-model="responseForm[index]"
                    :required="question.required"
                  />
                  <span>Oui</span>
                </label>
                <label class="radio-option">
                  <input 
                    type="radio" 
                    :name="`question_${index}`"
                    value="Non"
                    v-model="responseForm[index]"
                    :required="question.required"
                  />
                  <span>Non</span>
                </label>
              </div>
            </div>
          </div>

          <div class="respondent-info">
            <h4>Informations du répondant (optionnel)</h4>
            <div class="respondent-fields">
              <div class="form-group">
                <label for="respondent-name">Nom</label>
                <input 
                  id="respondent-name"
                  v-model="respondentInfo.name"
                  type="text"
                  class="form-input"
                  placeholder="Votre nom"
                />
              </div>
              <div class="form-group">
                <label for="respondent-email">Email</label>
                <input 
                  id="respondent-email"
                  v-model="respondentInfo.email"
                  type="email"
                  class="form-input"
                  placeholder="votre.email@exemple.com"
                />
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="resetForm" class="secondary-btn">Réinitialiser</button>
            <button type="submit" class="primary-btn">
              <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
              </svg>
              Soumettre la réponse
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Liste des réponses -->
    <div class="responses-list-section">
      <div class="section-header">
        <h3>Réponses reçues</h3>
        <div class="filters">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Rechercher dans les réponses..."
            class="search-input"
          />
        </div>
      </div>

      <div class="responses-grid">
        <div v-for="response in filteredResponses" :key="response.id" class="response-card">
          <div class="response-header">
            <h4>{{ response.surveyTitle }}</h4>
            <div class="response-meta">
              <span class="response-date">{{ response.date }}</span>
              <span v-if="response.respondent" class="respondent">{{ response.respondent }}</span>
            </div>
          </div>
          
          <div class="response-content">
            <div v-for="(answer, qIndex) in response.answers" :key="qIndex" class="answer-item">
              <div class="question">{{ answer.question }}</div>
              <div class="answer">{{ answer.response }}</div>
            </div>
          </div>

          <div class="response-actions">
            <button @click="viewResponse(response)" class="action-btn view">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
              </svg>
              Voir détails
            </button>
            <button @click="deleteResponse(response.id)" class="action-btn delete">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
              Supprimer
            </button>
          </div>
        </div>
      </div>

      <div v-if="filteredResponses.length === 0" class="no-responses">
        <svg class="no-data-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
        </svg>
        <p>Aucune réponse trouvée.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Question {
  text: string
  type: string
  options: string[]
  required: boolean
}

interface Survey {
  id: number
  title: string
  description: string
  questions: Question[]
}

interface Response {
  id: number
  surveyId: number
  surveyTitle: string
  answers: { question: string; response: string }[]
  respondent?: string
  email?: string
  date: string
}

const selectedSurvey = ref('')
const surveyToAnswer = ref('')
const searchQuery = ref('')
const currentSurveyQuestions = ref<Question[]>([])
const responseForm = ref<Record<number, any>>({})
const respondentInfo = ref({
  name: '',
  email: ''
})

const availableSurveys = ref<Survey[]>([
  {
    id: 1,
    title: 'Satisfaction Client 2024',
    description: 'Enquête annuelle de satisfaction des clients',
    questions: [
      { text: 'Comment évaluez-vous notre service ?', type: 'rating', options: [], required: true },
      { text: 'Recommanderiez-vous nos services ?', type: 'yesno', options: [], required: true },
      { text: 'Commentaires supplémentaires', type: 'text', options: [], required: false }
    ]
  },
  {
    id: 2,
    title: 'Feedback Produit',
    description: 'Retours sur notre nouveau produit',
    questions: [
      { text: 'Que pensez-vous du design ?', type: 'radio', options: ['Excellent', 'Bon', 'Moyen', 'Mauvais'], required: true },
      { text: 'Quelles fonctionnalités utilisez-vous le plus ?', type: 'checkbox', options: ['Feature A', 'Feature B', 'Feature C'], required: false }
    ]
  }
])

const responses = ref<Response[]>([
  {
    id: 1,
    surveyId: 1,
    surveyTitle: 'Satisfaction Client 2024',
    answers: [
      { question: 'Comment évaluez-vous notre service ?', response: '4' },
      { question: 'Recommanderiez-vous nos services ?', response: 'Oui' },
      { question: 'Commentaires supplémentaires', response: 'Très bon service, continuez ainsi !' }
    ],
    respondent: 'Jean Dupont',
    email: 'jean.dupont@exemple.fr',
    date: '28/03/2024 14:30'
  },
  {
    id: 2,
    surveyId: 2,
    surveyTitle: 'Feedback Produit',
    answers: [
      { question: 'Que pensez-vous du design ?', response: 'Excellent' },
      { question: 'Quelles fonctionnalités utilisez-vous le plus ?', response: 'Feature A, Feature C' }
    ],
    respondent: 'Marie Martin',
    date: '27/03/2024 16:45'
  },
  {
    id: 3,
    surveyId: 1,
    surveyTitle: 'Satisfaction Client 2024',
    answers: [
      { question: 'Comment évaluez-vous notre service ?', response: '5' },
      { question: 'Recommanderiez-vous nos services ?', response: 'Oui' }
    ],
    date: '26/03/2024 10:15'
  }
])

const filteredResponses = computed(() => {
  let filtered = responses.value

  if (selectedSurvey.value) {
    filtered = filtered.filter(r => r.surveyId === parseInt(selectedSurvey.value))
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(r => 
      r.surveyTitle.toLowerCase().includes(query) ||
      r.respondent?.toLowerCase().includes(query) ||
      r.answers.some(a => 
        a.question.toLowerCase().includes(query) ||
        a.response.toLowerCase().includes(query)
      )
    )
  }

  return filtered
})

const getCurrentSurvey = () => {
  return availableSurveys.value.find(s => s.id === parseInt(surveyToAnswer.value))
}

const loadSurveyQuestions = () => {
  const survey = getCurrentSurvey()
  if (survey) {
    currentSurveyQuestions.value = survey.questions
    responseForm.value = {}
  } else {
    currentSurveyQuestions.value = []
  }
}

const updateCheckboxResponse = (questionIndex: number, option: string, event: Event) => {
  const target = event.target as HTMLInputElement
  if (!responseForm.value[questionIndex]) {
    responseForm.value[questionIndex] = []
  }
  
  if (target.checked) {
    responseForm.value[questionIndex].push(option)
  } else {
    const index = responseForm.value[questionIndex].indexOf(option)
    if (index > -1) {
      responseForm.value[questionIndex].splice(index, 1)
    }
  }
}

const resetForm = () => {
  responseForm.value = {}
  respondentInfo.value = { name: '', email: '' }
  surveyToAnswer.value = ''
  currentSurveyQuestions.value = []
}

const submitResponse = () => {
  const survey = getCurrentSurvey()
  if (!survey) return

  const answers = currentSurveyQuestions.value.map((question, index) => ({
    question: question.text,
    response: Array.isArray(responseForm.value[index]) 
      ? responseForm.value[index].join(', ')
      : responseForm.value[index] || 'Non répondu'
  }))

  const newResponse: Response = {
    id: Date.now(),
    surveyId: survey.id,
    surveyTitle: survey.title,
    answers,
    respondent: respondentInfo.value.name || undefined,
    email: respondentInfo.value.email || undefined,
    date: new Date().toLocaleString('fr-FR')
  }

  responses.value.push(newResponse)
  resetForm()
  alert('Réponse soumise avec succès !')
}

const viewResponse = (response: Response) => {
  alert(`Affichage détaillé de la réponse #${response.id}`)
}

const deleteResponse = (responseId: number) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer cette réponse ?')) {
    responses.value = responses.value.filter(r => r.id !== responseId)
  }
}
</script>

<style scoped>
.responses {
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

.header-actions {
  display: flex;
  gap: 1rem;
}

.survey-select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  min-width: 200px;
}

.response-form-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.response-form-section h3 {
  margin: 0 0 1.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

.survey-selector {
  margin-bottom: 2rem;
}

.survey-selector label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  width: 100%;
  max-width: 400px;
}

.survey-info {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: #f0f9ff;
  border-radius: 8px;
  border-left: 4px solid #3b82f6;
}

.survey-info h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.survey-info p {
  margin: 0;
  color: #6b7280;
}

.answer-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.question-block {
  padding: 1.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background-color: #fafafa;
}

.question-header {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.question-number {
  font-weight: 600;
  color: #3b82f6;
  flex-shrink: 0;
}

.question-text {
  flex: 1;
  font-weight: 500;
  color: #1f2937;
}

.required {
  color: #dc2626;
  font-weight: 600;
}

.answer-input {
  margin-left: 1.5rem;
}

.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  min-height: 100px;
  resize: vertical;
}

.radio-group, .checkbox-group, .yesno-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.radio-option, .checkbox-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.radio-option:hover, .checkbox-option:hover {
  background-color: #f3f4f6;
}

.radio-option input, .checkbox-option input {
  margin: 0;
}

.rating-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.rating-scale {
  display: flex;
  gap: 1rem;
}

.rating-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}

.rating-option input {
  margin-bottom: 0.5rem;
}

.rating-number {
  font-weight: 600;
  color: #374151;
}

.rating-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
  color: #6b7280;
}

.respondent-info {
  padding: 1.5rem;
  background-color: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.respondent-info h4 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
}

.respondent-fields {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
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

.form-input {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
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

.btn-icon {
  width: 18px;
  height: 18px;
}

.responses-list-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

.search-input {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  min-width: 300px;
}

.responses-grid {
  display: grid;
  gap: 1.5rem;
}

.response-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  transition: box-shadow 0.2s;
}

.response-card:hover {
  box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.1);
}

.response-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.response-header h4 {
  margin: 0;
  font-weight: 600;
  color: #1f2937;
}

.response-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.response-content {
  margin-bottom: 1rem;
}

.answer-item {
  margin-bottom: 1rem;
}

.answer-item:last-child {
  margin-bottom: 0;
}

.question {
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.25rem;
}

.answer {
  color: #1f2937;
  padding-left: 1rem;
}

.response-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
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

.action-btn.delete {
  background-color: #fee2e2;
  color: #dc2626;
}

.action-btn.delete:hover {
  background-color: #fecaca;
}

.no-responses {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.no-data-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 1rem;
  color: #d1d5db;
}

@media (max-width: 767px) {
  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .search-input {
    min-width: auto;
  }
  
  .respondent-fields {
    grid-template-columns: 1fr;
  }
  
  .response-header {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .response-meta {
    align-items: flex-start;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>