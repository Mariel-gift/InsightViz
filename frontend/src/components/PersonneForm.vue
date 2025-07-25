<template>
  <div class="campagne-page">
    <div class="header">
      <h1>Gestion des personnes</h1>
      <button @click="openModal" class="create-btn">Ajouter une personne</button>
    </div>

    <div class="search-container">
      <div class="input-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
      </div>
      <input type="text" v-model="searchQuery" placeholder="Rechercher..." class="search-bar" />
    </div>

    <table class="campagne-table">
      <thead>
        <tr>
          <th>Nom</th>
          <th>Région</th>
          <th>Email</th>
          <th>Téléphone</th>
          <th>Type</th>
          <th>Taille</th>
          <th>Secteur</th>
          <th>Actions</th>  <!-- Nouvelle colonne -->
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in filteredPersonnes" :key="p.id">
          <td>{{ p.nom }}</td>
          <td>{{ p.region }}</td>
          <td>{{ p.email_contact }}</td>
          <td>{{ p.telephone }}</td>
          <td>{{ p.type }}</td>
          <td>{{ p.taille_entreprise }}</td>
          <td>{{ p.secteur_activite }}</td>
          <td>
            <button @click="editPersonne(p)" class="action-btn edit" title="Modifier">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 20h9" />
                <path d="M16.5 3.5a2.1 2.1 0 1 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
              </svg>
            </button>

            <button @click="deletePersonne(p.id)" class="action-btn delete" title="Supprimer">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6" />
                <path d="M19 6l-1 14H6L5 6" />
                <path d="M10 11v6" />
                <path d="M14 11v6" />
                <path d="M9 6V4h6v2" />
              </svg>
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal création / édition -->
    <div v-if="modalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h2>{{ isEditing ? "Modifier une personne" : "Ajouter une personne" }}</h2>
        <form @submit.prevent="submitForm">
          <input v-model="form.nom" placeholder="Nom" required class="input-field" />
          <input v-model="form.region" placeholder="Région" class="input-field" />
          <input v-model="form.email_contact" placeholder="Email" type="email" class="input-field" />
          <input v-model="form.telephone" placeholder="Téléphone" class="input-field" />

          <select v-model="form.type" required class="input-field">
            <option value="" disabled>-- Type --</option>
            <option value="transporteur">Transporteur</option>
            <option value="expediteur">Expéditeur</option>
          </select>

          <input
            v-if="form.type === 'transporteur'"
            v-model="form.taille_entreprise"
            placeholder="Taille entreprise"
            class="input-field"
          />

          <input
            v-if="form.type === 'expediteur'"
            v-model="form.secteur_activite"
            placeholder="Secteur d'activité"
            class="input-field"
          />

          <div class="modal-actions">
            <button type="submit" class="btn-primary" :disabled="loading">
              <span v-if="loading">Veuillez patienter...</span>
              <span v-else>{{ isEditing ? "Enregistrer" : "Créer" }}</span>
            </button>
            <button type="button" @click="closeModal" class="btn-cancel">Annuler</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from '../axios';

const personnes = ref([]);
const modalOpen = ref(false);
const searchQuery = ref('');
const loading = ref(false);
const isEditing = ref(false);
const selectedId = ref(null);

const form = ref({
  nom: '',
  region: '',
  email_contact: '',
  telephone: '',
  type: '',
  taille_entreprise: '',
  secteur_activite: ''
});

watch(
  () => form.value.type,
  (newType) => {
    if (newType === 'transporteur') form.value.secteur_activite = '';
    if (newType === 'expediteur') form.value.taille_entreprise = '';
  }
);

const fetchPersonnes = async () => {
  try {
    const res = await axios.get('/personnes');
    personnes.value = res.data;
  } catch (error) {
    alert("Erreur de chargement des personnes");
  }
};

const submitForm = async () => {
  loading.value = true;
  try {
    if (isEditing.value && selectedId.value) {
      await axios.put(`/personnes/${selectedId.value}`, form.value);
    } else {
      await axios.post('/personnes', form.value);
    }
    await fetchPersonnes();
    closeModal();
  } catch (error) {
    alert("Erreur lors de l'enregistrement");
  } finally {
    loading.value = false;
  }
};

const openModal = () => {
  resetForm();
  modalOpen.value = true;
  isEditing.value = false;
  selectedId.value = null;
};

const editPersonne = (personne) => {
  form.value = { ...personne };
  isEditing.value = true;
  selectedId.value = personne.id;
  modalOpen.value = true;
};

const deletePersonne = async (id) => {
  if (confirm("Voulez-vous supprimer cette personne ?")) {
    try {
      await axios.delete(`/personnes/${id}`);
      await fetchPersonnes();
    } catch (error) {
      alert("Erreur lors de la suppression");
    }
  }
};

const closeModal = () => {
  modalOpen.value = false;
  resetForm();
  isEditing.value = false;
  selectedId.value = null;
};

const resetForm = () => {
  form.value = {
    nom: '',
    region: '',
    email_contact: '',
    telephone: '',
    type: '',
    taille_entreprise: '',
    secteur_activite: ''
  };
};

const filteredPersonnes = computed(() => {
  const q = searchQuery.value.toLowerCase();
  return personnes.value.filter((p) => 
    p.nom.toLowerCase().includes(q) ||
    (p.region && p.region.toLowerCase().includes(q)) ||
    (p.type && p.type.toLowerCase().includes(q))
  );
});

onMounted(() => {
  fetchPersonnes();
});
</script>


<style scoped>
.campagne-page {
  padding: 2rem;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  max-width: 1200px;
  margin: 80px auto 2rem; /* 80px pour laisser place navbar fixe */
  color: #2c3e50;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.create-btn {
  background: #6a11cb;
  color: white;
  padding: 0.5rem 1.25rem;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
}

.create-btn:hover {
  background: #530fa8;
}

.search-bar {
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  width: 300px;
  margin-bottom: 1rem;
}

.campagne-table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 0 12px rgb(106 17 203 / 0.15);
  border-radius: 12px;
  overflow: hidden;
}

.campagne-table th,
.campagne-table td {
  text-align: left;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #eee;
  font-size: 0.95rem;
}

.campagne-table th {
  background: #6a11cb;
  color: white;
  font-weight: 600;
}

.campagne-table tr:hover {
  background: #f5f0ff;
}

.action-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #6a11cb;
  margin-right: 0.5rem;
  transition: color 0.3s;
}

.action-btn.danger {
  color: #e74c3c;
}

.action-btn:hover {
  color: #530fa8;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(57, 42, 106, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  color: #2c3e50;
}

.modal-content h2 {
  margin-bottom: 1rem;
  font-weight: 700;
}

.input-field {
  width: 100%;
  padding: 0.5rem 0.75rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
  font-family: inherit;
}

.label {
  font-weight: 600;
  margin-bottom: 0.3rem;
  display: block;
  color: #444;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.btn-primary {
  background: #6a11cb;
  color: rgb(250, 248, 248);
  padding: 0.6rem 1.5rem;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 700;
  transition: background-color 0.3s;
  flex: 1;
}

.btn-primary:hover {
  background: #530fa8;
}

.btn-cancel {
  background: #e74c3c;
  color: white;
  padding: 0.6rem 1.5rem;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 700;
  flex: 1;
  transition: background-color 0.3s;
}

.btn-cancel:hover {
  background: #c0392b;
}
@media (max-width: 768px) {
  .campagne-table thead {
    display: none;
  }

  .campagne-table, 
  .campagne-table tbody, 
  .campagne-table tr, 
  .campagne-table td {
    display: block;
    width: 100%;
  }

  .campagne-table tr {
    margin-bottom: 1rem;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    padding: 1rem;
  }

  .campagne-table td {
    text-align: right;
    padding-left: 50%;
    position: relative;
    border: none;
    border-bottom: 1px solid #eee;
  }

  .campagne-table td::before {
    content: attr(data-label);
    position: absolute;
    left: 1rem;
    top: 0.75rem;
    font-weight: bold;
    color: #6a11cb;
    text-align: left;
  }

  .campagne-table td:last-child {
    border-bottom: none;
  }
}
.search-container {
  position: relative;
  width: 100%;
  max-width: 400px;
  margin: auto;
}

.input-icon {
  position: absolute;
  top: 50%;
  left: 12px;
  transform: translateY(-50%);
  pointer-events: none;
  color: #777;
}

.search-bar {
  width: 100%;
  padding: 10px 10px 10px 40px; /* espace pour l'icône */
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 16px;
  outline: none;
}

@media (max-width: 600px) {
  .search-bar {
    font-size: 14px;
  }
}
.btn-primary:disabled {
  background: #a084d7;
  cursor: not-allowed;
  opacity: 0.7;
}
.action-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 4px 8px;
  margin-right: 6px;
  border-radius: 4px;
  transition: background-color 0.2s ease-in-out;
  color: #6a11cb;
}
.action-btn:hover {
  background-color: #e1d9ff;
}
.action-btn.delete {
  color: #e74c3c;
}
.action-btn.delete:hover {
  background-color: #fbeaea;
}
</style>

