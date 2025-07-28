<template>
  <div class="page-wrapper">
    <!-- === ENTÊTE === -->
    <div class="top-actions">
      <h2>Utilisateurs (hors Admin)</h2>
      <button class="btn-primary" @click="openAddModal">
        <svg width="20" height="20" viewBox="0 0 24 24">
          <path fill="currentColor" d="M12 5v14m-7-7h14" />
        </svg>
        Ajouter utilisateur
      </button>
    </div>

    <!-- === BARRE DE RECHERCHE === -->
    <div class="search-container">
      <div class="input-icon">
        <svg width="20" height="20" viewBox="0 0 24 24">
          <path fill="currentColor" d="M9.5 3a6.5 6.5 0 0 1 5.28 10.36l4.43 4.43-1.42 1.42-4.43-4.43A6.5 6.5 0 1 1 9.5 3z"/>
        </svg>
        <input type="text" v-model="search" placeholder="Rechercher utilisateur..." />
      </div>
    </div>

    <!-- === TABLEAU DES UTILISATEURS === -->
    <table class="styled-table">
      <thead>
        <tr>
          <th>Nom</th>
          <th>Email</th>
          <th>Rôle</th>
          <th>Créé le</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in filteredUsers" :key="u.id">
          <td>{{ u.full_name }}</td>
          <td>{{ u.email }}</td>
          <td>{{ u.role }}</td>
          <td>{{ new Date(u.created_at).toLocaleDateString() }}</td>
          <td>
            <button class="edit-btn" @click="openEditForm(u)">✏️</button>
            <button class="delete-btn" @click="deleteUser(u.id)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- === MODALE FORMULAIRE AJOUT === -->
    <div v-if="showAddModal" class="modal-overlay">
      <div class="modal-content">
        <h3>Ajouter un utilisateur</h3>
        <form @submit.prevent="submitAddForm">
          <div class="form-group">
            <label>Nom complet</label>
            <input v-model="formAdd.full_name" required />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="formAdd.email" type="email" required />
          </div>
          <div class="form-group">
            <label>Mot de passe</label>
            <input v-model="formAdd.password" type="password" required />
          </div>
          <div class="form-group">
            <label>Rôle</label>
            <select v-model="formAdd.role">
              <option value="user">Utilisateur</option>
              <option value="superadmin">Superadmin</option>
            </select>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">Ajouter</button>
            <button type="button" @click="closeModal" class="btn-secondary">Annuler</button>
          </div>
        </form>
      </div>
    </div>

    <!-- === FORMULAIRE MODIFICATION HORS MODALE === -->
    <div v-if="showEditForm" class="outside-form">
      <h3>Modifier utilisateur</h3>
      <form @submit.prevent="submitEditForm">
        <div class="form-group">
          <label>Nom complet</label>
          <input v-model="formEdit.full_name" required />
        </div>
        <div class="form-group">
          <label>Email</label>
          <input v-model="formEdit.email" type="email" required />
        </div>
        <div class="form-group">
          <label>Rôle</label>
          <select v-model="formEdit.role">
            <option value="user">Utilisateur</option>
            <option value="superadmin">Superadmin</option>
          </select>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary">Mettre à jour</button>
          <button type="button" @click="showEditForm = false" class="btn-secondary">Annuler</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "../axios";

export default {
  data() {
    return {
      users: [],
      search: "",
      showAddModal: false,
      showEditForm: false,
      formAdd: {
        full_name: "",
        email: "",
        password: "",
        role: "user",
      },
      formEdit: {
        id: null,
        full_name: "",
        email: "",
        role: "user",
      },
    };
  },
  computed: {
    filteredUsers() {
      return this.users.filter(u =>
        u.full_name.toLowerCase().includes(this.search.toLowerCase()) ||
        u.email.toLowerCase().includes(this.search.toLowerCase())
      );
    },
  },
  methods: {
    async fetchUsers() {
      const res = await axios.get("/api/users");
      this.users = res.data;
    },
    openAddModal() {
      this.showAddModal = true;
    },
    closeModal() {
      this.showAddModal = false;
    },
    openEditForm(user) {
      this.formEdit = { ...user };
      this.showEditForm = true;
    },
    async submitAddForm() {
      await axios.post("/api/users", this.formAdd);
      this.fetchUsers();
      this.closeModal();
    },
    async submitEditForm() {
      await axios.put(`/api/users/${this.formEdit.id}`, this.formEdit);
      this.fetchUsers();
      this.showEditForm = false;
    },
    async deleteUser(id) {
      if (confirm("Supprimer cet utilisateur ?")) {
        await axios.delete(`/api/users/${id}`);
        this.fetchUsers();
      }
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>

<style scoped>
/* ========== STRUCTURE GLOBALE ========== */
.page-wrapper {
  padding: 2rem;
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  min-height: 100vh;
  color: white;
  font-family: 'Segoe UI', sans-serif;
}

/* ========== TITRE ET BOUTON D'ACTION ========== */
.top-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #ffffff;
  color: #6a11cb;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: 0.3s ease;
}

.btn-primary:hover {
  background: #ecebff;
}

/* ========== BARRE DE RECHERCHE ========== */
.search-container {
  margin-bottom: 1.5rem;
}

.input-icon {
  position: relative;
}

.input-icon svg {
  position: absolute;
  top: 10px;
  left: 10px;
  color: #999;
}

.input-icon input {
  padding: 0.5rem 0.75rem 0.5rem 2.5rem;
  width: 100%;
  border-radius: 8px;
  border: none;
  outline: none;
  font-size: 1rem;
}

/* ========== TABLEAU ========== */
.styled-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  color: #333;
  border-radius: 10px;
  overflow: hidden;
}

.styled-table thead {
  background-color: #6a11cb;
  color: white;
}

.styled-table th,
.styled-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.styled-table tbody tr:hover {
  background-color: #f5f5f5;
}

.edit-btn,
.delete-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  margin-right: 0.5rem;
}

.edit-btn:hover {
  color: #2575fc;
}

.delete-btn:hover {
  color: red;
}

/* ========== MODALE AJOUT UTILISATEUR ========== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(10, 10, 10, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content {
  background: white;
  color: #333;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
}

/* ========== FORMULAIRE ========== */
form .form-group {
  margin-bottom: 1.2rem;
}

form label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

form input,
form select {
  width: 100%;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

/* ========== ACTIONS DU FORMULAIRE ========== */
.form-actions {
  margin-top: 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-secondary {
  background: #eee;
  color: #333;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
}

.btn-secondary:hover {
  background: #ddd;
}

/* ========== FORMULAIRE EN DEHORS DE LA MODALE (MODIF) ========== */
.outside-form {
  margin-top: 2rem;
  padding: 1.5rem;
  background: white;
  color: #333;
  border-radius: 12px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
}
</style>

