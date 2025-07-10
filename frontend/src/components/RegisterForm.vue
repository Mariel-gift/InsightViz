<template>
  <div class="register-form">
    <div class="form-header">
      <h2 class="form-title">Rejoindre InsightViz</h2>
      <p class="form-subtitle">Créez votre compte pour commencer l'analyse</p>
    </div>

    <form @submit.prevent="handleRegister" class="form">
      <div class="form-group">
        <label class="form-label">Nom complet</label>
        <div class="input-wrapper">
          <div class="input-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <input
            v-model="form.fullName"
            type="text"
            placeholder="Jean Dupont"
            class="form-input"
            :class="{ 'error': errors.fullName }"
            @blur="validateFullName"
            @input="clearError('fullName')"
          >
        </div>
        <div v-if="errors.fullName" class="error-message">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          {{ errors.fullName }}
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Entreprise</label>
        <div class="input-wrapper">
          <div class="input-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 21h18"></path>
              <path d="M5 21V7l8-4v18"></path>
              <path d="M19 21V11l-6-4"></path>
            </svg>
          </div>
          <input
            v-model="form.company"
            type="text"
            placeholder="Nom de votre entreprise"
            class="form-input"
            :class="{ 'error': errors.company }"
            @blur="validateCompany"
            @input="clearError('company')"
          >
        </div>
        <div v-if="errors.company" class="error-message">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          {{ errors.company }}
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Adresse email professionnelle</label>
        <div class="input-wrapper">
          <div class="input-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
              <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
          </div>
          <input
            v-model="form.email"
            type="email"
            placeholder="jean.dupont@entreprise.com"
            class="form-input"
            :class="{ 'error': errors.email }"
            @blur="validateEmail"
            @input="clearError('email')"
          >
        </div>
        <div v-if="errors.email" class="error-message">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          {{ errors.email }}
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Mot de passe</label>
        <div class="input-wrapper">
          <div class="input-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <circle cx="12" cy="16" r="1"></circle>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </div>
          <input
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Créer un mot de passe sécurisé"
            class="form-input"
            :class="{ 'error': errors.password }"
            @blur="validatePassword"
            @input="validatePassword"
          >
          <button
            type="button"
            class="password-toggle"
            @click="showPassword = !showPassword"
          >
            <svg v-if="!showPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
            <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
              <line x1="1" y1="1" x2="23" y2="23"></line>
            </svg>
          </button>
        </div>
        <div v-if="errors.password" class="error-message">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          {{ errors.password }}
        </div>
        <div v-if="form.password && !errors.password" class="password-strength">
          <div class="strength-bar">
            <div class="strength-fill" :class="passwordStrength.class" :style="{ width: passwordStrength.width }"></div>
          </div>
          <span class="strength-text">{{ passwordStrength.text }}</span>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Confirmer le mot de passe</label>
        <div class="input-wrapper">
          <div class="input-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <circle cx="12" cy="16" r="1"></circle>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </div>
          <input
            v-model="form.confirmPassword"
            :type="showConfirmPassword ? 'text' : 'password'"
            placeholder="Confirmer votre mot de passe"
            class="form-input"
            :class="{ 'error': errors.confirmPassword }"
            @blur="validateConfirmPassword"
            @input="clearError('confirmPassword')"
          >
          <button
            type="button"
            class="password-toggle"
            @click="showConfirmPassword = !showConfirmPassword"
          >
            <svg v-if="!showConfirmPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
            <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
              <line x1="1" y1="1" x2="23" y2="23"></line>
            </svg>
          </button>
        </div>
        <div v-if="errors.confirmPassword" class="error-message">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          {{ errors.confirmPassword }}
        </div>
      </div>

      <div class="form-options">
        <label class="checkbox-wrapper">
          <input v-model="form.agreeToTerms" type="checkbox" class="checkbox">
          <span class="checkmark"></span>
          J'accepte les <a href="#" class="terms-link">conditions d\'utilisation</a> et la <a href="#" class="terms-link">politique de confidentialité</a>
        </label>
        
        <label class="checkbox-wrapper">
          <input v-model="form.newsletter" type="checkbox" class="checkbox">
          <span class="checkmark"></span>
          Recevoir les actualités produit et conseils d'analyse
        </label>
      </div>

      <button 
        type="submit" 
        class="submit-btn"
        :class="{ loading: isLoading }"
        :disabled="isLoading || !form.agreeToTerms"
      >
        <span v-if="!isLoading">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          Créer mon compte
        </span>
        <div v-else class="loading-spinner"></div>
      </button>
    </form>

    <div class="form-footer">
      <p>Déjà un compte ? 
        <button @click="$emit('switch-to-login')" class="link-btn">Se connecter</button>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { authService } from '../services/api';

const emit = defineEmits(['switch-to-login'])

const form = reactive({
  fullName: '',
  company: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreeToTerms: false,
  newsletter: false
})

const errors = reactive({
  fullName: '',
  company: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const isLoading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const passwordStrength = computed(() => {
  const password = form.password
  if (!password) return { class: '', width: '0%', text: '' }

  let score = 0

  if (password.length >= 8) score += 1
  if (/[A-Z]/.test(password)) score += 1
  if (/[a-z]/.test(password)) score += 1
  if (/\d/.test(password)) score += 1
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score += 1

  const strength = {
    0: { class: 'very-weak', width: '20%', text: 'Très faible' },
    1: { class: 'weak', width: '40%', text: 'Faible' },
    2: { class: 'fair', width: '60%', text: 'Moyen' },
    3: { class: 'good', width: '80%', text: 'Bon' },
    4: { class: 'strong', width: '100%', text: 'Fort' },
    5: { class: 'very-strong', width: '100%', text: 'Très fort' }
  }

  return strength[score] || strength[0]
})

const validateFullName = () => {
  if (!form.fullName.trim()) {
    errors.fullName = 'Le nom complet est requis'
  } else if (form.fullName.trim().length < 2) {
    errors.fullName = 'Le nom doit contenir au moins 2 caractères'
  } else {
    errors.fullName = ''
  }
}

const validateCompany = () => {
  if (!form.company.trim()) {
    errors.company = 'Le nom de l\'entreprise est requis'
  } else if (form.company.trim().length < 2) {
    errors.company = 'Le nom de l\'entreprise doit contenir au moins 2 caractères'
  } else {
    errors.company = ''
  }
}

const validateEmail = () => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.email) {
    errors.email = 'L\'adresse email est requise'
  } else if (!emailPattern.test(form.email)) {
    errors.email = 'Veuillez entrer une adresse email valide'
  } else {
    errors.email = ''
  }
}

const validatePassword = () => {
  if (!form.password) {
    errors.password = 'Le mot de passe est requis'
  } else if (form.password.length < 8) {
    errors.password = 'Le mot de passe doit contenir au moins 8 caractères'
  } else {
    errors.password = ''
  }
  
  if (form.confirmPassword) {
    validateConfirmPassword()
  }
}

const validateConfirmPassword = () => {
  if (!form.confirmPassword) {
    errors.confirmPassword = 'Veuillez confirmer votre mot de passe'
  } else if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Les mots de passe ne correspondent pas'
  } else {
    errors.confirmPassword = ''
  }
}

const clearError = (field) => {
  errors[field] = ''
}

// === LA SEULE FONCTION HANDLE REGISTER CORRECTE ===
const handleRegister = async () => {
  // 1. Lancer toutes les validations
  validateFullName();
  validateCompany();
  validateEmail();
  validatePassword();
  validateConfirmPassword();
  
  // 2. S'arrêter s'il y a une erreur de validation
  if (Object.values(errors).some(error => error)) {
    return;
  }

  // 3. Vérifier que les conditions sont acceptées
  if (!form.agreeToTerms) {
    return;
  }

  // 4. Lancer le chargement et appeler l'API
  isLoading.value = true;
  
  try {
    // Appel au service API
    const response = await authService.register(form);
    console.log('Inscription réussie:', response.data.message);
    
    // Émettre l'événement pour basculer vers le formulaire de connexion
    emit('switch-to-login');

  } catch (error) {
    // Gérer les erreurs venant du backend
    console.error('Erreur d\'inscription:', error.response ? error.response.data : 'Erreur réseau');
    
    if (error.response && error.response.status === 409) {
        errors.email = 'Cette adresse email est déjà utilisée.';
    } else {
        errors.confirmPassword = "Une erreur est survenue lors de l'inscription.";
    }
  } finally {
    // Arrêter le chargement dans tous les cas
    isLoading.value = false;
  }
};
</script>

<style scoped>
.register-form {
  width: 100%;
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.form-subtitle {
  color: #64748b;
  font-size: 1rem;
  margin: 0;
}

.form {
  width: 100%;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  color: #9ca3af;
  z-index: 2;
  pointer-events: none;
}

.form-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #ffffff;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.form-input.error {
  border-color: #ef4444;
  background: #fef2f2;
}

.form-input::placeholder {
  color: #9ca3af;
}

.password-toggle {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  transition: color 0.3s ease;
  z-index: 2;
}

.password-toggle:hover {
  color: #3b82f6;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.password-strength {
  margin-top: 0.75rem;
}

.strength-bar {
  width: 100%;
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.strength-fill {
  height: 100%;
  transition: all 0.3s ease;
  border-radius: 3px;
}

.strength-fill.very-weak {
  background: #ef4444;
}

.strength-fill.weak {
  background: #f97316;
}

.strength-fill.fair {
  background: #eab308;
}

.strength-fill.good {
  background: #22c55e;
}

.strength-fill.strong,
.strength-fill.very-strong {
  background: #10b981;
}

.strength-text {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.form-options {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.checkbox-wrapper {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  font-size: 0.875rem;
  color: #64748b;
  line-height: 1.4;
}

.checkbox {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  margin-right: 0.75rem;
  margin-top: 0.1rem;
  position: relative;
  transition: all 0.3s ease;
  background: white;
  flex-shrink: 0;
}

.checkbox:checked + .checkmark {
  background: #3b82f6;
  border-color: #3b82f6;
}

.checkbox:checked + .checkmark::after {
  content: "✓";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 0.75rem;
  font-weight: bold;
}

.terms-link {
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.3s ease;
}

.terms-link:hover {
  color: #2563eb;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
}

.submit-btn:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.form-footer {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.form-footer p {
  color: #64748b;
  margin: 0;
}

.link-btn {
  color: #3b82f6;
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.link-btn:hover {
  color: #2563eb;
}

@media (max-width: 640px) {
  .form-title {
    font-size: 1.5rem;
  }
  
  .form-group {
    margin-bottom: 1.25rem;
  }
}
</style>