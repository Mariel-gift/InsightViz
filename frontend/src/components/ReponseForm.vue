<template>
  <div class="form-container">
    <h2>Soumettre une réponse</h2>

    <form @submit.prevent="submitForm">
      <!-- Enquête concernée -->
      <div class="form-group">
        <label for="enquete">Enquête :</label>
        <select id="enquete" v-model="form.enquete_id" required>
          <option value="" disabled>— Sélectionner —</option>
          <option v-for="e in enquetes" :key="e.id" :value="e.id">
            {{ e.titre }}
          </option>
        </select>
      </div>

      <!-- Type de répondant -->
      <div class="form-group">
        <label for="type">Type de répondant :</label>
        <select id="type" v-model="form.type_repondant" required>
          <option value="" disabled>— Sélectionner —</option>
          <option value="transporteur">Transporteur</option>
          <option value="expediteur">Expéditeur</option>
        </select>
      </div>

      <!-- ID répondant -->
      <div class="form-group">
        <label for="id_repondant">ID du répondant :</label>
        <input
          id="id_repondant"
          v-model.number="form.id_repondant"
          type="number"
          min="1"
          required
        />
      </div>

      <!-- Données de réponse (JSON) -->
      <div class="form-group">
        <label for="donnees">Données de réponse (JSON) :</label>
        <textarea
          id="donnees"
          v-model="form.donnees_reponse"
          rows="6"
          placeholder='{"question_1": "Oui", "question_2": 4}'
          required
        ></textarea>
      </div>

      <!-- Message d’erreur JSON (si besoin) -->
      <p v-if="jsonError" class="json-error">
        Format JSON invalide : {{ jsonError }}
      </p>

      <!-- Bouton envoyer -->
      <button class="btn-primary" type="submit">Enregistrer</button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, watch } from 'vue';
import axios from 'axios' ; // instance axios préconfigurée

/* ===== Données ===== */
const enquetes = ref([]);
const jsonError = ref('');
const form = reactive({
  enquete_id: '',
  type_repondant: '',
  id_repondant: '',
  donnees_reponse: ''
});

/* ===== Validation JSON ===== */
watch(() => form.donnees_reponse, (val) => {
  try {
    JSON.parse(val);
    jsonError.value = '';
  } catch (e) {
    jsonError.value = e.message;
  }
});

/* ===== Soumission ===== */
const submitForm = async () => {
  if (jsonError.value) {
    alert('Veuillez corriger le JSON avant de soumettre.');
    return;
  }

  try {
    await axios.post('/reponses-enquetes', {
      ...form,
      donnees_reponse: JSON.parse(form.donnees_reponse) // envoyer comme objet
    });
    alert('Réponse enregistrée avec succès !');

    // reset
    form.enquete_id = '';
    form.type_repondant = '';
    form.id_repondant = '';
    form.donnees_reponse = '';
  } catch (error) {
    console.error(error);
    alert("Une erreur s'est produite lors de l'enregistrement.");
  }
};

/* ===== Récupérer les enquêtes ===== */
onMounted(async () => {
  try {
    const { data } = await axios.get('/enquetes');
    enquetes.value = data;
  } catch (error) {
    console.error(error);
  }
});
</script>

<style scoped>
.form-container {
  max-width: 650px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 1rem;
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  color: #fff;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.form-container h2 {
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1.6rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.25rem;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  color: #333;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: 2px solid #fff;
}

.json-error {
  margin-top: -0.75rem;
  margin-bottom: 0.75rem;
  font-size: 0.9rem;
  color: #ffbebe;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  background: #fff;
  color: #2575fc;
  transition: background 0.2s ease-in-out;
}

.btn-primary:hover {
  background: #e5e5e5;
}
</style>
