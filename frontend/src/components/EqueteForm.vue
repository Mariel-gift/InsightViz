<template>
  <div class="page-wrapper">
    <!-- Bouton créer enquête -->
    <div class="top-actions">
      <button class="btn-primary" @click="openFormModal">
        Créer une enquête
      </button>
    </div>

    <!-- Barre de recherche -->
    <div class="search-container" style="margin: 1rem 0;">
      <div class="input-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
      </div>
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Rechercher une enquête..."
        class="search-bar"
      />
    </div>

    <!-- Tableau enquêtes -->
    <div class="table-wrapper">
      <h2>Liste des enquêtes</h2>
      <table v-if="filteredEnquetes.length" class="enquetes-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Titre</th>
            <th>Créée le</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="e in filteredEnquetes" :key="e.id">
            <td>{{ e.id }}</td>
            <td>{{ e.titre }}</td>
            <td>{{ formatDate(e.date_creation) }}</td>
            <td>
              <span :class="['badge', e.answered ? 'answered' : 'pending']">
                {{ e.answered ? 'Répondu' : 'En attente' }}
              </span>
            </td>
            <td class="action-icons">
  <button class="icon-btn" title="Voir questions" @click="viewQuestions(e.id)">
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  </button>
  <button class="icon-btn" title="Modifier" @click="loadEnquete(e.id)">
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4h2m3.707 1.293l3 3a1 1 0 01.293.707V20a1 1 0 01-1 1H5a1 1 0 01-1-1V4a1 1 0 011-1h6a1 1 0 01.707.293l4 4z" />
    </svg>
  </button>
  <button class="icon-btn" title="Supprimer" @click="deleteEnquete(e.id)">
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
    </svg>
  </button>
</td>

          </tr>
        </tbody>
      </table>
      <p v-else class="empty">Aucune enquête enregistrée.</p>
    </div>

    <!-- MODALE FORMULAIRE CREATION / MODIF ENQUETE -->
    <div v-if="showFormModal" class="modal-overlay" @click.self="closeFormModal">
      <div class="modal large-modal">
        <h2>{{ editEnqId ? "Modifier une enquête" : "Créer une enquête" }}</h2>

        <form @submit.prevent="submitForm">
          <!-- Titre -->
          <div class="form-group">
            <label for="titre">Titre *</label>
            <input id="titre" v-model="form.titre" type="text" required />
          </div>

          <!-- Campagne -->
          <div class="form-group">
            <label for="campagne">Campagne liée</label>
            <select id="campagne" v-model="form.campagne_id">
              <option disabled value="">-- Sélectionnez une campagne --</option>
              <option v-for="c in campagnes" :key="c.id" :value="c.id">{{ c.nom }}</option>
            </select>
          </div>

          <!-- Questions -->
          <div class="questions-header">
            <span>Questions</span>
            <button type="button" class="btn-secondary" @click="openAddModal">Ajouter une question</button>
          </div>

          <ul class="questions-list" v-if="questions.length">
            <li v-for="(q, i) in questions" :key="i">
              <span class="q-text">{{ q }}</span>
              <div class="q-actions">
                <button type="button" class="action-btn" @click="openEditModal(i)">Modifier</button>
                <button type="button" class="action-btn" @click="deleteQuestion(i)">Supprimer</button>
              </div>
            </li>
          </ul>
          <p v-else class="empty">Aucune question pour l’instant.</p>

          <button class="btn-primary" type="submit">{{ editEnqId ? 'Mettre à jour' : 'Créer' }}</button>
        </form>

        <!-- Bouton fermer modal -->
        <button class="btn-cancel close-btn" @click="closeFormModal">Fermer</button>
      </div>
    </div>

    <!-- Modale ajout/modif question (petite modal dans modal formulaire) -->
    <div v-if="showQuestionModal" class="modal-overlay" @click.self="closeQuestionModal">
      <div class="modal">
        <h3>{{ modalTitle }}</h3>
        <input v-model="newQuestion" type="text" placeholder="Saisis la question ici…" autofocus />
        <div class="modal-actions">
          <button class="btn-cancel" @click="closeQuestionModal">Annuler</button>
          <button class="btn-primary" @click="saveQuestion">Valider</button>
        </div>
      </div>
    </div>

    <!-- Modale voir questions -->


    <div v-if="showViewModal" class="modal-overlay" @click.self="closeViewModal">
      <div class="modal">
        <h3>Questions de l’enquête #{{ selectedEnqueteId }}</h3>
        <ul v-if="selectedQuestions.length">
          <li v-for="q in selectedQuestions" :key="q.id">
            {{ q.ordre }}. {{ q.texte }}
          </li>
        </ul>
        <p v-else>Aucune question trouvée pour cette enquête.</p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="closeViewModal">Fermer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import axios from "../axios";

const campagnes = ref([]);
const enquetes = ref([]);
const questions = ref([]);

const showFormModal = ref(false);
const showQuestionModal = ref(false);
const showViewModal = ref(false);

const newQuestion = ref("");
const editIndex = ref(null);
const selectedQuestions = ref([]);
const selectedEnqueteId = ref(null);
const editEnqId = ref(null);

const form = reactive({
  titre: "",
  campagne_id: null,
});

const searchQuery = ref("");

function openFormModal() {
  resetForm();
  showFormModal.value = true;
}

function closeFormModal() {
  showFormModal.value = false;
  resetForm();
}

function openAddModal() {
  editIndex.value = null;
  newQuestion.value = "";
  showQuestionModal.value = true;
}

function openEditModal(i) {
  editIndex.value = i;
  newQuestion.value = questions.value[i].replace(/^Q\d+:\s*/, "");
  showQuestionModal.value = true;
}

function closeQuestionModal() {
  showQuestionModal.value = false;
  newQuestion.value = "";
}

function saveQuestion() {
  const txt = newQuestion.value.trim();
  if (!txt) {
    alert("Veuillez saisir une question.");
    return;
  }
  if (editIndex.value === null) {
    questions.value.push(`Q${questions.value.length + 1}: ${txt}`);
  } else {
    questions.value[editIndex.value] = `Q${editIndex.value + 1}: ${txt}`;
  }
  closeQuestionModal();
}

function deleteQuestion(i) {
  questions.value.splice(i, 1);
  questions.value = questions.value.map((q, idx) =>
    q.replace(/^Q\d+:/, `Q${idx + 1}:`)
  );
}
const submitForm = async () => {
  console.log("submitForm appelé");
  console.log("editEnqId.value =", editEnqId.value);
  console.log("form.titre =", form.titre);
  console.log("form.campagne_id =", form.campagne_id);
  console.log("questions =", questions.value);

  if (!form.titre.trim()) {
    alert("Le titre est obligatoire.");
    return;
  }
  if (!form.campagne_id) {
    alert("La campagne liée est obligatoire.");
    return;
  }
  if (questions.value.length === 0) {
    alert("Veuillez ajouter au moins une question.");
    return;
  }

  const payload = {
    titre: form.titre.trim(),
    campagne_id: form.campagne_id,
    questions: questions.value.map((q, index) => {
      const texte = q.replace(/^Q\d+:\s*/, "");
      return {
        ordre: index + 1,
        texte: texte,
      };
    }),
  };

  try {
    if (editEnqId.value) {
      console.log("Envoi PUT pour mise à jour enquête ID:", editEnqId.value);
      await axios.put(`/enquetes/${editEnqId.value}`, payload);
      alert("Enquête mise à jour ✅");
    } else {
      console.log("Envoi POST pour création nouvelle enquête");
      const { data } = await axios.post(`/enquetes`, payload);
      alert("Enquête créée ✅");
      selectedEnqueteId.value = data.id;
    }

    await fetchEnquetes();
    closeFormModal();
  } catch (error) {
    console.error("Erreur lors de la création/mise à jour de l'enquête", error);
    alert("Erreur lors de la sauvegarde. Voir console.");
  }
};
async function deleteEnquete(id) {
  const confirmed = confirm("Voulez-vous vraiment supprimer cette enquête ?");
  if (!confirmed) return;

  try {
    await axios.delete(`/enquetes/${id}`);
    alert("Enquête supprimée.");
    await fetchEnquetes();
  } catch (e) {
    console.error("Erreur lors de la suppression:", e);
    alert("Erreur lors de la suppression.");
  }
}



function resetForm() {
  form.titre = "";
  form.campagne_id = null;
  questions.value = [];
  editEnqId.value = null;
  searchQuery.value = "";
}

async function fetchEnquetes() {
  try {
    const { data } = await axios.get("/enquetes");
    enquetes.value = data;
  } catch (error) {
    console.error(error);
  }
}

const filteredEnquetes = computed(() => {
  if (!searchQuery.value) return enquetes.value;
  return enquetes.value.filter((e) =>
    e.titre.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

onMounted(async () => {
  try {
    const [c, e] = await Promise.all([axios.get("/campagnes"), axios.get("/enquetes")]);
    campagnes.value = c.data;
    enquetes.value = e.data;
  } catch (e) {
    console.error(e);
  }
});

async function viewQuestions(enqueteId) {
  try {
    const { data } = await axios.get(`/enquetes/${enqueteId}/questions`);
    selectedQuestions.value = data;
    selectedEnqueteId.value = enqueteId;
    showViewModal.value = true;
  } catch (error) {
    console.error("Erreur lors du chargement des questions:", error);
    alert("Impossible de charger les questions.");
  }
}

function closeViewModal() {
  showViewModal.value = false;
  selectedQuestions.value = [];
  selectedEnqueteId.value = null;
}

const modalTitle = computed(() =>
  editIndex.value === null ? "Nouvelle question" : "Modifier la question"
);

async function loadEnquete(id) {
  try {
    const [{ data: eq }, { data: qs }] = await Promise.all([
      axios.get(`/enquetes/${id}`),
      axios.get(`/enquetes/${id}/questions`),
    ]);
    form.titre = eq.titre;
    form.campagne_id = eq.campagne_id;
    questions.value = qs.map((q) => `Q${q.ordre}: ${q.texte}`);
    editEnqId.value = id;
    showFormModal.value = true; // Ouvrir la modale avec données chargées
  } catch (e) {
    console.error(e);
    alert("Impossible de charger l’enquête.");
  }
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString();
}
</script>

<style scoped>
.page-wrapper {
  padding: 2rem;
  max-width: 1200px;
  margin: 80px auto 2rem;
  color: #2c3e50;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}
.top-actions {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 1rem;
}
.btn-primary {
  background: hsl(269, 85%, 43%);
  color: white;
  padding: 0.6rem 1.5rem;
  border: none;
  border-radius: 25px;
  font-weight: 700;
  cursor: pointer;
}
.btn-primary:hover {
  background: #530fa8;
}
.btn-secondary {
  background: hsl(269, 85%, 43%);
  color: rgb(240, 240, 245);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
}
.btn-secondary:hover {
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
}
.btn-cancel:hover {
  background: #c0392b;
}
.close-btn {
  margin-top: 1rem;
  width: 100%;
}
/* Tableau */
.table-wrapper h2 {
  margin-top: 2rem;
  margin-bottom: 1rem;
}
.enquetes-table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 0 12px rgb(106 17 203 / 0.15);
  border-radius: 12px;
  overflow: hidden;
}
.enquetes-table th,
.enquetes-table td {
  text-align: left;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #eee;
  font-size: 0.95rem;
}
.enquetes-table th {
  background: #6a11cb;
  color: white;
  font-weight: 600;
}
.enquetes-table tr:hover {
  background: #f5f0ff;
}
.badge {
  padding: 0.25rem 0.6rem;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #fff;
}
.badge.answered {
  background: #2ecc71;
}
.badge.pending {
  background: #f1c40f;
}
/* Modal */
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
.modal {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  color: #2c3e50;
}
.large-modal {
  max-width: 700px;
}
.modal h2,
.modal h3 {
  margin-bottom: 1rem;
  font-weight: 700;
  text-align: center;
}
.modal input,
.modal select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  margin-bottom: 1.25rem;
  font-size: 1rem;
}
.questions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 1rem 0 0.5rem;
  font-weight: 600;
}
.questions-list {
  list-style: none;
  padding: 0;
  margin-bottom: 1.5rem;
}
.questions-list li {
  background: rgba(106, 17, 203, 0.15);
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}
.q-actions {
  display: flex;
  gap: 0.5rem;
}
.action-btn {
  background: rgba(255, 255, 255, 0.3);
  color: #6a11cb;
  border: none;
  border-radius: 0.3rem;
  padding: 0.25rem 0.6rem;
  font-size: 0.9rem;
  cursor: pointer;
}
.action-btn:hover {
  background: rgba(255, 255, 255, 0.6);
}
.empty {
  color: #555;
  font-style: italic;
  margin-top: 1rem;
  text-align: center;
}
/* Recherche */
.search-container {
  position: relative;
  max-width: 400px;
}
.input-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  color: #6a11cb;
}
.search-bar {
  width: 100%;
  padding: 0.5rem 1rem 0.5rem 2.5rem;
  border: 2px solid #6a11cb;
  border-radius: 25px;
  font-size: 1rem;
  color: #2c3e50;
  outline: none;
  transition: border-color 0.3s ease;
}
.search-bar:focus {
  border-color: #2575fc;
}
.icon-btn {
  background: transparent;
  border: none;
  margin-right: 0.4rem;
  cursor: pointer;
  color: #333;
  transition: color 0.2s ease;
}

.icon-btn:hover {
  color: #e74c3c;
}

</style>
