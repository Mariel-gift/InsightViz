<template>
  <div class="form-container">
    <h2>Créer une personne</h2>

    <form @submit.prevent="submitForm">
      <!-- Nom -->
      <div class="form-group">
        <label for="nom">Nom :</label>
        <input id="nom" v-model="form.nom" type="text" required />
      </div>

      <!-- Région -->
      <div class="form-group">
        <label for="region">Région :</label>
        <input id="region" v-model="form.region" type="text" />
      </div>

      <!-- E‑mail -->
      <div class="form-group">
        <label for="email">E‑mail de contact :</label>
        <input id="email" v-model="form.email_contact" type="email" />
      </div>

      <!-- Téléphone -->
      <div class="form-group">
        <label for="telephone">Téléphone :</label>
        <input id="telephone" v-model="form.telephone" type="tel" />
      </div>

      <!-- Type -->
      <div class="form-group">
        <label for="type">Type :</label>
        <select id="type" v-model="form.type" required>
          <option value="" disabled>— Sélectionner —</option>
          <option value="transporteur">Transporteur</option>
          <option value="expediteur">Expéditeur</option>
        </select>
      </div>

      <!-- Taille de l’entreprise (transporteur) -->
      <div class="form-group" v-if="isTransporteur">
        <label for="taille">Taille de l’entreprise :</label>
        <input
          id="taille"
          v-model="form.taille_entreprise"
          type="text"
          placeholder="ex. : 51‑200"
        />
      </div>

      <!-- Secteur d’activité (expéditeur) -->
      <div class="form-group" v-if="isExpediteur">
        <label for="secteur">Secteur d’activité :</label>
        <input
          id="secteur"
          v-model="form.secteur_activite"
          type="text"
          placeholder="ex. : Agroalimentaire"
        />
      </div>

      <!-- Bouton envoyer -->
      <button class="btn-primary" type="submit">Enregistrer</button>
    </form>
  </div>
</template>

<script setup>
import { reactive, computed, watch } from 'vue';
import axios from 'axios' ;  // Instancie axios avec baseURL = '/api'

/* ===== Données réactives ===== */
const form = reactive({
  nom: '',
  region: '',
  email_contact: '',
  telephone: '',
  type: '',
  taille_entreprise: '',
  secteur_activite: ''
});

/* ===== Composés (affichage conditionnel) ===== */
const isTransporteur = computed(() => form.type === 'transporteur');
const isExpediteur  = computed(() => form.type === 'expediteur');

/* ===== Réinitialiser le champ non pertinent lorsqu’on change de type ===== */
watch(
  () => form.type,
  (newType) => {
    if (newType === 'transporteur') form.secteur_activite = '';
    if (newType === 'expediteur')  form.taille_entreprise = '';
  }
);

/* ===== Soumission ===== */
const submitForm = async () => {
  try {
    await axios.post('/personnes', form); // POST /api/personnes
    alert('Personne créée avec succès !');

    // Remise à zéro
    Object.assign(form, {
      nom: '',
      region: '',
      email_contact: '',
      telephone: '',
      type: '',
      taille_entreprise: '',
      secteur_activite: ''
    });
  } catch (error) {
    console.error(error);
    alert("Une erreur s'est produite lors de l'enregistrement.");
  }
};
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
.form-group select {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  color: #333;
}

.form-group input:focus,
.form-group select:focus {
  outline: 2px solid #fff;
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
