<!-- Dashboard.vue -->
<template>
  <div class="dashboard-page">
    <!-- ===== NAVBAR ===== -->
    <nav class="navbar">
      <div class="brand">InsightViz</div>

      <ul class="nav-links">
        <li><a href="#" @click.prevent="scrollTo('accueil')">Accueil</a></li>
        <li><a href="#" @click.prevent="scrollTo('apropos')">À propos</a></li>
        <li><a href="#" @click.prevent="scrollTo('contact')">Contact</a></li>
      </ul>

      <button class="login-btn" @click="openModal">Connexion / S’inscrire</button>
    </nav>

    <!-- ===== MODALE AUTH ===== -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="auth-modal">
        <div class="tabs">
          <button :class="{active: tab==='register'}" @click="tab='register'">S’inscrire</button>
          <button :class="{active: tab==='login'}"    @click="tab='login'">Se connecter</button>
        </div>

        <!-- ----- INSCRIPTION ----- -->
        <form v-if="tab==='register'" @submit.prevent="submitRegister">
          <div class="form-row">
            <label>Nom d’utilisateur *</label>
            <input v-model="registerForm.full_name" required />
          </div>
          <div class="form-row">
            <label>Email *</label>
            <input type="email" v-model="registerForm.email" autocomplete="username" required />
          </div>
          <div class="form-row">
            <label>Rôle *</label>
            <select v-model="registerForm.role" required>
              <option value="">— Choisir —</option>
              <option value="admin">Admin</option>
              <option value="user">Utilisateur</option>
            </select>
          </div>
          <div class="form-row">
            <label>Mot de passe *</label>
            <input type="password" v-model="registerForm.password" autocomplete="new-password" required />
          </div>
          <button type="submit" class="btn-primary">Créer le compte</button>
        </form>

        <!-- ----- CONNEXION ----- -->
        <form v-else @submit.prevent="submitLogin">
          <div class="form-row">
            <label>E‑mail *</label>
            <input type="email" v-model="loginForm.email" autocomplete="username" required />
          </div>
          <div class="form-row">
            <label>Mot de passe *</label>
            <input type="password" v-model="loginForm.password" autocomplete="current-password" required />
          </div>
          <button class="btn-primary">Se connecter</button>
        </form>
      </div>
    </div>

    <!-- ===== CONTENU PRINCIPAL ===== -->
    <main class="main-content">
      <!-- -------- ACCUEIL -------- -->
      <section id="accueil" class="home-section">
        <h1 class="home-title">
          Bienvenue sur <span>InsightViz</span>
        </h1>
        <p class="home-subtitle">
          Système d’analyse automatisée et de visualisation<br />
          des enquêtes logistiques.
        </p>
        <button class="cta-button" @click="scrollTo('apropos')">Découvrir</button>
      </section>

      <!-- -------- À PROPOS -------- -->
      <section id="apropos" class="apropos-section">
        <h2 class="apropos-title">Pourquoi choisir InsightViz&nbsp;?</h2>

        <div class="apropos-grid">
          <!-- Carte 1 -->
          <div class="apropos-card">
            <div class="apropos-icon">
              <!-- SVG "graph" -->
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke="currentColor" width="40" height="40" fill="none">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 3v18h18M8 17V9m5 8V5m5 12v-6"/>
              </svg>
            </div>
            <h3>Analyse automatisée</h3>
            <p>
              Statistiques et graphiques générés instantanément pour suivre vos
              enquêtes logistiques sans effort.
            </p>
          </div>

          <!-- Carte 2 -->
          <div class="apropos-card">
            <div class="apropos-icon">
              <!-- SVG "shield check" -->
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke="currentColor" width="40" height="40" fill="none">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3l7 4v5c0 5-3 9-7 10-4-1-7-5-7-10V7l7-4z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"/>
              </svg>
            </div>
            <h3>Données sécurisées</h3>
            <p>
              Hébergé sous Flask & PostgreSQL, InsightViz garantit la protection
              et la confidentialité de vos données.
            </p>
          </div>

          <!-- Carte 3 -->
          <div class="apropos-card">
            <div class="apropos-icon">
              <!-- SVG "bolt" -->
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke="currentColor" width="40" height="40" fill="none">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
            <h3>Visualisation rapide</h3>
            <p>
              Interface Vue 3 + Chart.js : visualisez vos campagnes et réponses
              en un clin d’œil, sur tous vos appareils.
            </p>
          </div>
        </div>
      </section>

      <!-- -------- CONTACT -------- -->
   <section id="contact" class="contact-section">
  <h2>Contactez-nous</h2>

  <div class="contact-row">
    <!-- Email -->
    <div class="contact-item">
      <svg class="icon" xmlns="http://www.w3.org/2000/svg" fill="none"
           viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 4h16v16H4z" />
        <polyline points="22,6 12,13 2,6" />
      </svg>
      <div>
        <h4>Email</h4>
        <p>connectiq@gmail.com</p>
      </div>
    </div>

    <!-- Téléphone -->
    <div class="contact-item">
      <svg class="icon" xmlns="http://www.w3.org/2000/svg" fill="none"
           viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M22 16.92v3a2 2 0 0 1-2.18 2
                 19.86 19.86 0 0 1-8.63-3.07
                 19.5 19.5 0 0 1-6-6
                 A19.86 19.86 0 0 1 2.08 4.18
                 2 2 0 0 1 4 2h3
                 a2 2 0 0 1 2 1.72
                 c.2 1.38.56 2.72 1.08 4
                 .36.9.12 1.94-.57 2.63l-1.27 1.27
                 a16 16 0 0 0 6 6l1.27-1.27
                 a2.36 2.36 0 0 1 2.63-.57
                 c1.28.52 2.62.88 4 1.08
                 A2 2 0 0 1 22 16.92z" />
      </svg>
      <div>
        <h4>Téléphone</h4>
        <p>034 65 182 56</p>
      </div>
    </div>

    <!-- Facebook -->
    <div class="contact-item">
      <svg class="icon" xmlns="http://www.w3.org/2000/svg"
           viewBox="0 0 24 24" fill="currentColor">
        <path
          d="M22 12a10 10 0 1 0-11.6 9.87v-6.99h-2.3v-2.88h2.3v-2.2
             c0-2.28 1.35-3.54 3.42-3.54.99 0 2.03.18 2.03.18v2.23h-1.14
             c-1.13 0-1.48.7-1.48 1.42v1.91h2.52l-.4 2.88h-2.12v6.99A10 10 0 0 0 22 12z" />
      </svg>
      <div>
        <h4>Facebook</h4>
        <p>Cyber ConnectiQ</p>
      </div>
    </div>

    <!-- Entreprise -->
    <div class="contact-item">
      <svg class="icon" xmlns="http://www.w3.org/2000/svg"
           viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 21h18M6 21V8a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13M9 21V10h6v11" />
      </svg>
      <div>
        <h4>Entreprise</h4>
        <p>ConnectiQ</p>
      </div>
    </div>
  </div>
</section>
<footer class="site-footer">
  <p>&copy; 2025 ConnectiQ – Tous droits réservés.</p>
</footer>

    </main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../axios'

/* --- Router & état --- */
const router = useRouter()
const showModal = ref(false)
const tab = ref('login')
const isLoading = ref(false)

/* --- Données des formulaires --- */
const loginForm = ref({ email: '', password: '' })
const registerForm = ref({
  full_name: '',
  email: '',
  password: '',
  role: '',
})

/* --- Modal controls --- */
const openModal = () => {
  tab.value = 'login'
  showModal.value = true
}
const closeModal = () => {
  showModal.value = false
}

/* --- Redirection par rôle --- */
const redirectByRole = (role) => {
  if (role === 'admin') {
    router.push({ name: 'admin' }) // Vers back-office
  } else {
    router.push({ name: 'dashboard' }) // Vers dashboard client
  }
}

/* --- Soumission inscription --- */
const submitRegister = async () => {
  if (isLoading.value) return
  isLoading.value = true
  try {
const response = await axios.post('/register', {
  full_name: registerForm.value.full_name,
  email: registerForm.value.email,
  password: registerForm.value.password,
  role: registerForm.value.role,
})


    alert(response.data.message)
    if (response.data.redirect === '/admin') {
      router.push({ name: 'admin' })
    } else {
      router.push({ name: 'dashboard' })
    }
  } catch (error) {
    const msg = error.response?.data?.error || 'Erreur lors de l’inscription.'
    alert(msg)
  } finally {
    isLoading.value = false
  }
}

/* --- Soumission connexion --- */
const submitLogin = async () => {
  if (isLoading.value) return
  isLoading.value = true
  try {
   const res = await axios.post('/login', {
  email: loginForm.value.email,
  password: loginForm.value.password
})

    const user = res.data.user

    if (!user || !user.role) throw new Error('Utilisateur non valide.')

    localStorage.setItem('user', JSON.stringify(user))
    alert(res.data.message)
    redirectByRole(user.role)
    closeModal()
  } catch (error) {
    alert("Erreur de connexion")
  } finally {
    isLoading.value = false
  }
}

/* --- Scroll fluide --- */
const scrollTo = (id) => {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>



<style scoped>
/* ===== Structure ===== */
.dashboard-page { display:flex; flex-direction:column; height:100vh; width:100vw; overflow:hidden; }
.main-content   { flex:1; overflow-y:auto; scroll-behavior:smooth; }

/* ===== Navbar ===== */
.navbar{
  position:fixed; top:0; left:0; right:0; height:64px; z-index:2000;
  display:flex; align-items:center; justify-content:space-between;
  padding:0 2rem; background:rgba(57,42,106,.85); backdrop-filter:blur(8px); color:#fff;
}
.brand{ font-size:1.5rem; font-weight:700 }
.nav-links{ display:flex; gap:1.5rem; list-style:none; margin:0; padding:0 }
.nav-links a{ color:#fff; text-decoration:none; font-weight:500 }
.nav-links a:hover{ text-decoration:underline }
.login-btn{ background:#fff; color:#6a11cb; font-weight:600; border:none;
  padding:.45rem 1rem; border-radius:20px; cursor:pointer; transition:transform .2s }
.login-btn:hover{ transform:scale(1.05) }

/* ===== Home ===== */
.home-section{
  height:100vh; width:100vw;
  background:url('@/assets/InsightViz.png') center/cover no-repeat;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  text-align:center; color:#fff; position:relative;
}
.home-section::before{ content:''; position:absolute; inset:0; background:rgba(0,0,0,.45); z-index:0 }
.home-section>*{ position:relative; z-index:1 }
.home-title{ font-size:3rem; font-weight:bold; margin-bottom:1rem }
.home-title span{ background:linear-gradient(to right,#a18cd1,#fbc2eb);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent }
.home-subtitle{ font-size:1.25rem; margin-bottom:2rem; max-width:700px }
.cta-button{ background:#fff; color:#6a11cb; padding:.75rem 2rem; border:none;
  border-radius:25px; cursor:pointer; transition:background .3s, transform .3s }
.cta-button:hover{ background:#f0f0f0; transform:scale(1.05) }

/* ===== Apropos ===== */
.apropos-section{
  background:#f9f9fe; padding:4rem 2rem; border-radius:12px;
  box-shadow:0 2px 8px rgba(0,0,0,.05); max-width:1200px; margin:0 auto;
  text-align:center;
}
.apropos-title{ font-size:2rem; font-weight:bold; color:#2c3e50; margin-bottom:3rem }
.apropos-grid{ display:grid; gap:2rem; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)) }

@keyframes fadeInUp{
  from{ opacity:0; transform:translateY(30px) }
  to{   opacity:1; transform:translateY(0) }
}
.apropos-card{
  background:#fff; padding:1.8rem; border-radius:1rem;
  box-shadow:0 2px 10px rgba(0,0,0,.05); transition:transform .2s;
  opacity:0; animation:fadeInUp .6s ease forwards;
}
.apropos-card:hover{ transform:translateY(-5px) }
.apropos-card:nth-child(1){ animation-delay:.2s }
.apropos-card:nth-child(2){ animation-delay:.4s }
.apropos-card:nth-child(3){ animation-delay:.6s }

.apropos-icon{ font-size:2.5rem; color:#2575fc; margin-bottom:1rem }
.apropos-card h3{ font-size:1.2rem; color:#2c3e50; margin-bottom:.8rem }
.apropos-card p{ font-size:.95rem; color:#555; line-height:1.55 }

/* ===== Contact ===== */
.contact-section{
  min-height:100vh; padding-top:100px; text-align:center; display:flex; flex-direction:column;
  justify-content:center; align-items:center; background:#fff;
}
.contact-section h2{ font-size:2rem; margin-bottom:1rem; color:#2c3e50 }
.contact-section p { font-size:1rem; color:#555 }

/* ===== Modale ===== */
.modal-overlay{
  position:fixed; inset:0; background:rgba(0,0,0,.55); display:flex;
  align-items:center; justify-content:center; z-index:3000;
}
.auth-modal{
  background:#fff; border-radius:12px; padding:2rem; width:90%; max-width:400px;
  box-shadow:0 8px 20px rgba(0,0,0,.25);
}
.tabs{ display:flex; margin-bottom:1.5rem }
.tabs button{ flex:1; padding:.75rem 0; border:none; cursor:pointer; font-weight:600 }
.tabs button.active{ background:#6a11cb; color:#fff; border-radius:6px 6px 0 0 }
.tabs button:not(.active){ background:#f0f0f6 }
.form-row{ display:flex; flex-direction:column; margin-bottom:1rem }
.form-row label{ font-weight:600; margin-bottom:.4rem }
.form-row input,.form-row select{ padding:.6rem; border:1px solid #ccc; border-radius:6px }
.btn-primary{ width:100%; padding:.75rem; background:#6a11cb; color:#fff; border:none;
  border-radius:8px; font-weight:bold; cursor:pointer }
.btn-primary:hover{ opacity:.9 }
.contact-section {
  background: #fff;
  padding: 4rem 2rem;
  text-align: center;
}

.contact-section {
  background: #fff;
  padding: 2rem;
  text-align: center;
  margin-top: 1rem;
}

.contact-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  margin-top: 1.5rem;
}

.contact-item {
  display: flex;
  align-items: center;
  background: #f9f9fe;
  padding: 1rem 1.2rem;
  border-radius: 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  gap: 0.8rem;
  min-width: 230px;
}

.icon {
  width: 24px;
  height: 24px;
  color: #6a11cb;
  flex-shrink: 0;
}

.contact-item h4 {
  margin: 0;
  font-size: 0.95rem;
  color: #2c3e50;
}

.contact-item p {
  margin: 0.2rem 0 0;
  font-size: 0.88rem;
  color: #555;
}
.site-footer {
  background: rgba(57, 42, 106, 0.9);
  color: #fff;
  text-align: center;
  padding: 1rem 0;
  font-size: 0.9rem;
  margin-top: auto;
}




</style>
