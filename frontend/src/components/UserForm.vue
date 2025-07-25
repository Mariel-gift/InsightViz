<template>
  <div class="user-form-container">
    <!-- Bouton d'ajout -->
    <button @click="ouvrirAjoutModal" class="primary-btn">
      ➕ Ajouter un utilisateur
    </button>

    <!-- Barre de recherche -->
    <div class="search-bar">
      <input
        v-model="termeRecherche"
        type="text"
        placeholder="🔍 Rechercher un utilisateur..."
      />
    </div>

    <!-- Tableau des utilisateurs -->
    <table v-if="utilisateursFiltres.length" class="user-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nom</th>
          <th>Email</th>
          <th>Rôle</th>
          <th>Création</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in utilisateursFiltres" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.full_name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
          <td>{{ user.created_at }}</td>
          <td class="actions">
            <button @click="ouvrirModifierModal(user)" class="edit-btn">✏️</button>
            <button @click="ouvrirModal(user)" class="delete-btn">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else class="empty-msg">Aucun utilisateur trouvé.</p>

    <!-- Modal Ajout -->
    <div v-if="showAjoutModal" class="modal-overlay">
      <div class="modal-box">
        <h3>Ajouter un utilisateur</h3>
        <form @submit.prevent="ajouterUtilisateur" class="form">
          <div class="form-group">
            <label class="form-label">Nom</label>
            <input v-model="nouvelUtilisateur.full_name" type="text" placeholder="Nom complet" class="form-input" required />
          </div>

          <div class="form-group">
            <label class="form-label">Adresse email</label>
            <input v-model="nouvelUtilisateur.email" type="email" placeholder="email@exemple.com" class="form-input" required />
          </div>

          <div class="form-group">
            <label class="form-label">Mot de passe</label>
            <input v-model="nouvelUtilisateur.mot_de_passe" type="password" placeholder="Mot de passe" class="form-input" required />
          </div>

          <div class="form-group">
            <label class="form-label">Rôle</label>
            <select v-model="nouvelUtilisateur.role" class="form-input" required>
              <option disabled value="">-- Sélectionner --</option>
              <option value="admin">Admin</option>
              <option value="user">Utilisateur</option>
            </select>
          </div>

          <div class="modal-actions">
            <button type="submit" class="submit-btn">Ajouter</button>
            <button type="button" @click="fermerAjoutModal" class="cancel-btn">Annuler</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Modifier -->
    <div v-if="showEditModal" class="modal-overlay">
      <div class="modal-box">
        <h3>Modifier l'utilisateur</h3>
        <form @submit.prevent="modifierUtilisateur" class="form">
          <div class="form-group">
            <label class="form-label">Nom</label>
            <input v-model="utilisateurAModifier.full_name" type="text" class="form-input" required />
          </div>

          <div class="form-group">
            <label class="form-label">Email</label>
            <input v-model="utilisateurAModifier.email" type="email" class="form-input" required />
          </div>

          <div class="form-group">
            <label class="form-label">Rôle</label>
            <select v-model="utilisateurAModifier.role" class="form-input" required>
              <option value="admin">Admin</option>
              <option value="user">Utilisateur</option>
            </select>
          </div>

          <div class="modal-actions">
            <button type="submit" class="submit-btn">Enregistrer</button>
            <button type="button" @click="fermerEditModal" class="cancel-btn">Annuler</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Suppression -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-box">
        <p>⚠️Voulez-vous de supprimer <strong>{{ utilisateurASupprimer?.full_name }}</strong> ?</p>
        <div class="modal-actions">
          <button @click="confirmerSuppression" class="confirm-btn">Oui</button>
          <button @click="fermerModal" class="cancel-btn">Non</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from '../axios'

// État
const utilisateurs = ref([])
const termeRecherche = ref('')
const showModal = ref(false)
const showAjoutModal = ref(false)
const showEditModal = ref(false)

const utilisateurASupprimer = ref(null)
const utilisateurAModifier = ref({})
const nouvelUtilisateur = ref({ full_name: '', email: '', mot_de_passe: '', role: '' })

// Chargement des utilisateurs depuis l’API
const chargerUtilisateurs = async () => {
  try {
    const res = await axios.get('/api/users')
    utilisateurs.value = res.data
  } catch (err) {
    console.error("Erreur de chargement :", err)
  }
}
onMounted(chargerUtilisateurs)

// Filtrage utilisateurs
const utilisateursFiltres = computed(() => {
  const terme = termeRecherche.value.toLowerCase()
  return utilisateurs.value.filter(user =>
    user.full_name.toLowerCase().includes(terme) ||
    user.email.toLowerCase().includes(terme) ||
    user.role.toLowerCase().includes(terme)
  )
})

// Ajout
const ouvrirAjoutModal = () => showAjoutModal.value = true
const fermerAjoutModal = () => {
  showAjoutModal.value = false
  nouvelUtilisateur.value = { full_name: '', email: '', mot_de_passe: '', role: '' }
}
const ajouterUtilisateur = async () => {
  try {
    await axios.post('/api/users', {
      full_name: nouvelUtilisateur.value.full_name,
      email: nouvelUtilisateur.value.email,
      password: nouvelUtilisateur.value.mot_de_passe,
      role: nouvelUtilisateur.value.role,
    })
    fermerAjoutModal()
    chargerUtilisateurs()
  } catch (err) {
    console.error("Erreur ajout utilisateur :", err)
  }
}

// Modification
const ouvrirModifierModal = (user) => {
  utilisateurAModifier.value = { ...user }
  showEditModal.value = true
}
const fermerEditModal = () => {
  utilisateurAModifier.value = {}
  showEditModal.value = false
}
const modifierUtilisateur = async () => {
  try {
    await axios.put(`/api/users/${utilisateurAModifier.value.id}`, {
      full_name: utilisateurAModifier.value.full_name,
      email: utilisateurAModifier.value.email,
      role: utilisateurAModifier.value.role
    })
    fermerEditModal()
    chargerUtilisateurs()
  } catch (err) {
    console.error("Erreur modification :", err)
  }
}

// Suppression
const ouvrirModal = (user) => {
  utilisateurASupprimer.value = user
  showModal.value = true
}
const fermerModal = () => {
  utilisateurASupprimer.value = null
  showModal.value = false
}
const confirmerSuppression = async () => {
  try {
    await axios.delete(`/api/users/${utilisateurASupprimer.value.id}`)
    fermerModal()
    chargerUtilisateurs()
  } catch (err) {
    console.error("Erreur suppression :", err)
  }
}
</script>


<style scoped>
.user-form-container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2rem;
  background: linear-gradient(120deg, #f0f4ff, #ffffff);
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
  font-family: 'Segoe UI', sans-serif;
}

.primary-btn {
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  padding: 0.7rem 1.4rem;
  border: none;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  font-size: 1rem;
  margin-bottom: 1rem;
}
.primary-btn:hover {
  opacity: 0.95;
}

.search-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

.search-bar input {
  padding: 0.6rem 1rem;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 1rem;
  width: 300px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}

.user-table th, .user-table td {
  padding: 0.9rem;
  border: 1px solid #eee;
  font-size: 0.95rem;
  text-align: left;
}

.user-table th {
  background: #eef2ff;
  font-weight: bold;
}

.actions button {
  font-size: 1.2rem;
  background: none;
  border: none;
  cursor: pointer;
}

.edit-btn:hover { color: #16a34a; }
.delete-btn:hover { color: #dc2626; }

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-box {
  background: #fff;
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  font-weight: 600;
  margin-bottom: 0.3rem;
  display: block;
}

.form-input {
  width: 100%;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.submit-btn {
  background: #1c56d3;
  color: white;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}
.submit-btn:hover { background: #1d4ed8; }

.cancel-btn {
  background: #e5e7eb;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.confirm-btn {
  background: #5628d6;
  color: white;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.empty-msg {
  text-align: center;
  color: #888;
  margin-top: 2rem;
}
</style>
