<template>
  <div class="user-view">
    <div class="page-header">
      <h1 class="page-title">Gestion Utilisateur</h1>
      <p class="page-subtitle">Gérez votre profil et vos informations personnelles</p>
    </div>

    <div class="user-content">
      <div class="profile-card">
        <div class="profile-header">
          <div class="profile-avatar">
            <UserIcon class="avatar-icon" />
          </div>
          <div class="profile-info">
            <h2 class="user-name">{{ currentUser.name }}</h2>
            <p class="user-role">{{ currentUser.role }}</p>
            <p class="user-email">{{ currentUser.email }}</p>
          </div>
          <button @click="editProfile = true" class="edit-profile-btn">
            <PencilIcon class="btn-icon" />
            Modifier le profil
          </button>
        </div>

        <div class="profile-details">
          <div class="detail-group">
            <h3>Informations personnelles</h3>
            <div class="detail-item">
              <span class="detail-label">Nom complet:</span>
              <span class="detail-value">{{ currentUser.name }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Email:</span>
              <span class="detail-value">{{ currentUser.email }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Rôle:</span>
              <span class="detail-value">{{ currentUser.role }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Téléphone:</span>
              <span class="detail-value">{{ currentUser.phone }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Département:</span>
              <span class="detail-value">{{ currentUser.department }}</span>
            </div>
          </div>

          <div class="detail-group">
            <h3>Statistiques</h3>
            <div class="stats-grid">
              <div class="stat-item">
                <span class="stat-number">{{ userStats.surveysCreated }}</span>
                <span class="stat-label">Enquêtes créées</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ userStats.responsesReceived }}</span>
                <span class="stat-label">Réponses reçues</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ userStats.campaignsManaged }}</span>
                <span class="stat-label">Campagnes gérées</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de modification du profil -->
    <div v-if="editProfile" class="modal-overlay" @click="editProfile = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Modifier le profil</h3>
          <button @click="editProfile = false" class="close-btn">
            <XMarkIcon class="close-icon" />
          </button>
        </div>
        
        <form @submit.prevent="saveProfile" class="form">
          <div class="form-group">
            <label for="name" class="form-label">Nom complet</label>
            <input 
              id="name"
              v-model="editForm.name"
              type="text"
              required
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="email" class="form-label">Email</label>
            <input 
              id="email"
              v-model="editForm.email"
              type="email"
              required
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="phone" class="form-label">Téléphone</label>
            <input 
              id="phone"
              v-model="editForm.phone"
              type="tel"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="department" class="form-label">Département</label>
            <input 
              id="department"
              v-model="editForm.department"
              type="text"
              class="form-input"
            />
          </div>
          
          <div class="form-actions">
            <button type="button" @click="editProfile = false" class="cancel-btn">
              Annuler
            </button>
            <button type="submit" class="save-btn">
              Sauvegarder
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { UserIcon, PencilIcon, XMarkIcon } from '@heroicons/vue/24/outline'

const editProfile = ref(false)

const currentUser = reactive({
  name: 'Marie Dubois',
  email: 'marie.dubois@insightviz.com',
  role: 'Administrateur',
  phone: '+33 1 23 45 67 89',
  department: 'Analyses et études'
})

const userStats = {
  surveysCreated: 15,
  responsesReceived: 1285,
  campaignsManaged: 8
}

const editForm = reactive({
  name: currentUser.name,
  email: currentUser.email,
  phone: currentUser.phone,
  department: currentUser.department
})

const saveProfile = () => {
  Object.assign(currentUser, editForm)
  editProfile.value = false
}
</script>

<style scoped>
.user-view {
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

.profile-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.profile-header {
  padding: 2rem;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.profile-avatar {
  width: 5rem;
  height: 5rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-icon {
  width: 2.5rem;
  height: 2.5rem;
}

.profile-info {
  flex: 1;
}

.user-name {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
}

.user-role {
  font-size: 1rem;
  margin: 0 0 0.25rem 0;
  color: rgba(255, 255, 255, 0.8);
}

.user-email {
  font-size: 0.875rem;
  margin: 0;
  color: rgba(255, 255, 255, 0.7);
}

.edit-profile-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.edit-profile-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.btn-icon {
  width: 1rem;
  height: 1rem;
}

.profile-details {
  padding: 2rem;
}

.detail-group {
  margin-bottom: 2rem;
}

.detail-group:last-child {
  margin-bottom: 0;
}

.detail-group h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f3f4f6;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 500;
  color: #374151;
}

.detail-value {
  color: #6b7280;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.5rem;
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  transition: background 0.2s;
}

.close-btn:hover {
  background: #f3f4f6;
}

.close-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 500;
  color: #374151;
}

.form-input {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
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
}

.cancel-btn {
  padding: 0.75rem 1.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  background: white;
  color: #374151;
  cursor: pointer;
  transition: background 0.2s;
}

.cancel-btn:hover {
  background: #f9fafb;
}

.save-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  background: #10b981;
  color: white;
  cursor: pointer;
  transition: background 0.2s;
}

.save-btn:hover {
  background: #059669;
}
</style>