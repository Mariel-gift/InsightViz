<template>
  <div class="page-wrapper">
    <!-- ========== ENTÊTE ========== -->
    <div class="top-actions">
      <h2>Réponses aux enquêtes</h2>
      <button @click="openForm" class="btn-primary">Répondre à une enquête</button>
    </div>

    <!-- ========== BARRE DE RECHERCHE ========== -->
    <div class="search-container">
      <input v-model="search" type="text" placeholder="Rechercher..." class="search-bar" />
      <svg xmlns="http://www.w3.org/2000/svg" class="search-icon" width="20" height="20" viewBox="0 0 24 24">
        <path fill="currentColor" d="M21 20.3l-5.7-5.7a7 7 0 1 0-1.4 1.4L20.3 21zM4 10a6 6 0 1 1 12 0a6 6 0 0 1-12 0z" />
      </svg>
    </div>

    <!-- ========== TABLEAU DES RÉPONSES ========== -->
    <table class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Enquête</th>
          <th>Type</th>
          <th>Personne</th>
          <th>Données</th>
          <th>Date</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="reponse in filteredReponses" :key="reponse.id">
          <td>{{ reponse.id }}</td>
          <td>{{ reponse.enquete_id }}</td>
          <td>{{ reponse.type_repondant }}</td>
          <td>{{ reponse.personne_id }}</td>
          <td>{{ reponse.donnees_reponse }}</td>
          <td>{{ reponse.date_creation?.slice(0, 10) }}</td>
          <td class="actions">
            <!-- MODIFIER -->
            <button @click="editReponse(reponse)">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24">
                <path fill="currentColor" d="M5 19h14v2H5zM6 17h2l9-9-2-2-9 9v2z" />
              </svg>
            </button>
            <!-- SUPPRIMER -->
            <button @click="deleteReponse(reponse.id)">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24">
                <path fill="currentColor" d="M6 7h12v2H6zM10 11h4v8h-4z" />
              </svg>
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- ========== MODALE FORMULAIRE ========== -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h3>{{ editing ? "Modifier" : "Répondre à" }} une enquête</h3>
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="enquete_id">Enquête</label>
            <select v-model="form.enquete_id" required>
              <option v-for="e in enquetes" :key="e.id" :value="e.id">{{ e.titre }}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="type_repondant">Type de répondant</label>
            <input v-model="form.type_repondant" required />
          </div>
          <div class="form-group">
            <label for="personne_id">Personne ID</label>
            <input v-model="form.personne_id" type="number" required />
          </div>
          <div class="form-group">
            <label for="donnees_reponse">Données (JSON)</label>
            <textarea v-model="form.donnees_reponse" rows="3" required></textarea>
          </div>

          <div class="modal-actions">
            <button type="submit" class="btn-primary">{{ editing ? "Mettre à jour" : "Envoyer" }}</button>
            <button @click="closeForm" type="button" class="btn-cancel">Annuler</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  data() {
    return {
      reponses: [],
      enquetes: [],
      search: "",
      showModal: false,
      editing: false,
      form: {
        id: null,
        enquete_id: "",
        type_repondant: "",
        personne_id: "",
        donnees_reponse: "",
      },
    };
  },
  computed: {
    filteredReponses() {
      return this.reponses.filter((r) =>
        JSON.stringify(r).toLowerCase().includes(this.search.toLowerCase())
      );
    },
  },
  methods: {
    async fetchReponses() {
      const res = await axios.get("/reponses-enquetes");
      this.reponses = res.data;
    },
    async fetchEnquetes() {
      const res = await axios.get("/enquetes");
      this.enquetes = res.data;
    },
    openForm() {
      this.resetForm();
      this.showModal = true;
      this.editing = false;
    },
    closeForm() {
      this.showModal = false;
    },
    editReponse(reponse) {
      this.form = { ...reponse };
      this.showModal = true;
      this.editing = true;
    },
    async deleteReponse(id) {
      if (confirm("Confirmer la suppression ?")) {
        await axios.delete(`/reponses-enquetes/${id}`);
        this.fetchReponses();
      }
    },
    async submitForm() {
      const payload = {
        enquete_id: this.form.enquete_id,
        type_repondant: this.form.type_repondant,
        personne_id: this.form.personne_id,
        donnees_reponse: this.form.donnees_reponse,
      };
      if (this.editing) {
        await axios.put(`/reponses-enquetes/${this.form.id}`, payload);
      } else {
        await axios.post("/reponses-enquetes", payload);
      }
      this.closeForm();
      this.fetchReponses();
    },
    resetForm() {
      this.form = {
        id: null,
        enquete_id: "",
        type_repondant: "",
        personne_id: "",
        donnees_reponse: "",
      };
    },
  },
  mounted() {
    this.fetchReponses();
    this.fetchEnquetes();
  },
};
</script>

<style scoped>
.page-wrapper {
  max-width: 1000px;
  margin: auto;
  padding: 2rem;
}

.top-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-primary {
  background: linear-gradient(to right, #7b2ff7, #6454f0);
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
}

.search-container {
  position: relative;
  margin: 1rem 0;
}

.search-bar {
  padding: 0.5rem 2rem 0.5rem 2.5rem;
  width: 100%;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.search-icon {
  position: absolute;
  top: 50%;
  left: 8px;
  transform: translateY(-50%);
  color: #888;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  border: 1px solid #ccc;
  padding: 0.5rem;
  text-align: left;
}

.actions button {
  background: none;
  border: none;
  margin-right: 0.3rem;
  cursor: pointer;
  color: #333;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 2rem;
  width: 500px;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-cancel {
  background: #ccc;
  color: black;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
}
</style>
