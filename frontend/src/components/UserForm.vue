<template>
  <div class="users">
    <div class="page-header">
      <h2>Gestion des Utilisateurs</h2>
      <button @click="showAddForm = true" class="primary-btn">
        <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
        Ajouter un utilisateur
      </button>
    </div>

    <!-- Formulaire d'ajout/modification -->
    <div v-if="showAddForm" class="form-modal">
      <div class="form-container">
        <div class="form-header">
          <h3>{{ editingUser ? 'Modifier l\'utilisateur' : 'Nouvel Utilisateur' }}</h3>
          <button @click="closeForm" class="close-btn">&times;</button>
        </div>
        
        <form @submit.prevent="saveUser" class="user-form">
          <div class="form-grid">
            <div class="form-group">
              <label for="nom">Nom *</label>
              <input 
                id="nom" 
                v-model="userForm.nom" 
                type="text" 
                required 
                class="form-input"
                placeholder="Entrez le nom"
              />
            </div>
            
            <div class="form-group">
              <label for="prenom">Prénom *</label>
              <input 
                id="prenom" 
                v-model="userForm.prenom" 
                type="text" 
                required 
                class="form-input"
                placeholder="Entrez le prénom"
              />
            </div>
            
            <div class="form-group">
              <label for="email">Email *</label>
              <input 
                id="email" 
                v-model="userForm.email" 
                type="email" 
                required 
                class="form-input"
                placeholder="exemple@email.com"
              />
            </div>
            
            <div class="form-group">
              <label for="role">Rôle *</label>
              <select id="role" v-model="userForm.role" required class="form-select">
                <option value="">Sélectionner un rôle</option>
                <option value="Admin">Administrateur</option>
                <option value="Manager">Manager</option>
                <option value="User">Utilisateur</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="departement">Département</label>
              <input 
                id="departement" 
                v-model="userForm.departement" 
                type="text" 
                class="form-input"
                placeholder="Département"
              />
            </div>
            
            <div class="form-group">
              <label for="telephone">Téléphone</label>
              <input 
                id="telephone" 
                v-model="userForm.telephone" 
                type="tel" 
                class="form-input"
                placeholder="+33 1 23 45 67 89"
              />
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="closeForm" class="secondary-btn">Annuler</button>
            <button type="submit" class="primary-btn">
              {{ editingUser ? 'Modifier' : 'Ajouter' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Barre de recherche et filtres -->
    <div class="search-filters">
      <div class="search-bar">
        <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Rechercher des utilisateurs..."
          class="search-input"
        />
      </div>
      
      <div class="filters">
        <select v-model="roleFilter" class="filter-select">
          <option value="">Tous les rôles</option>
          <option value="Admin">Administrateur</option>
          <option value="Manager">Manager</option>
          <option value="User">Utilisateur</option>
        </select>
      </div>
    </div>

    <!-- Tableau des utilisateurs -->
    <div class="table-container">
      <table class="users-table">
        <thead>
          <tr>
            <th>Nom complet</th>
            <th>Email</th>
            <th>Rôle</th>
            <th>Département</th>
            <th>Date d'ajout</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id" class="table-row">
            <td>
              <div class="user-info">
                <img :src="user.avatar" :alt="user.nom" class="user-avatar" />
                <div>
                  <div class="user-name">{{ user.prenom }} {{ user.nom }}</div>
                  <div class="user-title">{{ user.telephone || 'N/A' }}</div>
                </div>
              </div>
            </td>
            <td>{{ user.email }}</td>
            <td>
              <span class="role-badge" :class="user.role.toLowerCase()">
                {{ user.role }}
              </span>
            </td>
            <td>{{ user.departement || 'N/A' }}</td>
            <td>{{ user.dateAjout }}</td>
            <td>
              <span class="status-badge" :class="user.statut.toLowerCase()">
                {{ user.statut }}
              </span>
            </td>
            <td>
              <div class="action-buttons">
                <button @click="editUser(user)" class="action-btn edit" title="Modifier">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                </button>
                <button @click="deleteUser(user.id)" class="action-btn delete" title="Supprimer">
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

interface User {
  id: number
  nom: string
  prenom: string
  email: string
  role: string
  departement: string
  telephone: string
  dateAjout: string
  statut: string
  avatar: string
}

const showAddForm = ref(false)
const editingUser = ref<User | null>(null)
const searchQuery = ref('')
const roleFilter = ref('')

const userForm = ref({
  nom: '',
  prenom: '',
  email: '',
  role: '',
  departement: '',
  telephone: ''
})

const users = ref<User[]>([
  {
    id: 1,
    nom: 'Dubois',
    prenom: 'Marie',
    email: 'marie.dubois@exemple.fr',
    role: 'Admin',
    departement: 'IT',
    telephone: '+33 1 23 45 67 89',
    dateAjout: '15/03/2024',
    statut: 'Actif',
    avatar: 'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=100'
  },
  {
    id: 2,
    nom: 'Martin',
    prenom: 'Pierre',
    email: 'pierre.martin@exemple.fr',
    role: 'Manager',
    departement: 'Marketing',
    telephone: '+33 1 23 45 67 90',
    dateAjout: '20/03/2024',
    statut: 'Actif',
    avatar: 'https://images.pexels.com/photos/697509/pexels-photo-697509.jpeg?auto=compress&cs=tinysrgb&w=100'
  },
  {
    id: 3,
    nom: 'Laurent',
    prenom: 'Sophie',
    email: 'sophie.laurent@exemple.fr',
    role: 'User',
    departement: 'Ventes',
    telephone: '+33 1 23 45 67 91',
    dateAjout: '25/03/2024',
    statut: 'Inactif',
    avatar: 'https://images.pexels.com/photos/712513/pexels-photo-712513.jpeg?auto=compress&cs=tinysrgb&w=100'
  }
])

const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchesSearch = !searchQuery.value || 
      user.nom.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      user.prenom.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesRole = !roleFilter.value || user.role === roleFilter.value
    
    return matchesSearch && matchesRole
  })
})

const closeForm = () => {
  showAddForm.value = false
  editingUser.value = null
  userForm.value = {
    nom: '',
    prenom: '',
    email: '',
    role: '',
    departement: '',
    telephone: ''
  }
}

const editUser = (user: User) => {
  editingUser.value = user
  userForm.value = {
    nom: user.nom,
    prenom: user.prenom,
    email: user.email,
    role: user.role,
    departement: user.departement,
    telephone: user.telephone
  }
  showAddForm.value = true
}

const saveUser = () => {
  if (editingUser.value) {
    // Modifier l'utilisateur existant
    const index = users.value.findIndex(u => u.id === editingUser.value!.id)
    if (index !== -1) {
      users.value[index] = {
        ...users.value[index],
        ...userForm.value
      }
    }
  } else {
    // Ajouter un nouvel utilisateur
    const newUser: User = {
      id: Date.now(),
      ...userForm.value,
      dateAjout: new Date().toLocaleDateString('fr-FR'),
      statut: 'Actif',
      avatar: 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=100'
    }
    users.value.push(newUser)
  }
  
  closeForm()
}

const deleteUser = (userId: number) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur ?')) {
    users.value = users.value.filter(u => u.id !== userId)
  }
}
</script>

<style scoped>
.users {
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
  max-width: 600px;
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

.user-form {
  padding: 1.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
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

.form-input, .form-select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
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
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.search-bar {
  position: relative;
  flex: 1;
  min-width: 300px;
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

.filters {
  display: flex;
  gap: 1rem;
}

.filter-select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  min-width: 150px;
}

.table-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th {
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

.users-table td {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
  vertical-align: middle;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-weight: 500;
  color: #1f2937;
}

.user-title {
  font-size: 0.875rem;
  color: #6b7280;
}

.role-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
}

.role-badge.admin {
  background-color: #fee2e2;
  color: #dc2626;
}

.role-badge.manager {
  background-color: #fef3c7;
  color: #d97706;
}

.role-badge.user {
  background-color: #e0e7ff;
  color: #4338ca;
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

.status-badge.inactif {
  background-color: #fee2e2;
  color: #dc2626;
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
  
  .search-filters {
    flex-direction: column;
  }
  
  .search-bar {
    min-width: auto;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .users-table {
    min-width: 800px;
  }
}
</style>