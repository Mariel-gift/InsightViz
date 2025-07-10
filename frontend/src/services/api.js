import axios from 'axios'

// Vérifie que la variable d'environnement est bien chargée
console.log('API base URL:', import.meta.env.VITE_API_BASE_URL)

// Crée une instance Axios avec la base URL dynamique
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Intercepteur pour ajouter automatiquement le token JWT dans les headers
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('accessToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

/* ===============================
   Authentification (Register/Login)
   =============================== */
export const authService = {
  register(userData) {
    const payload = {
      full_name: userData.fullName,
      company: userData.company,
      email: userData.email,
      password: userData.password,
      wants_newsletter: userData.newsletter,
      agree_to_terms: userData.agreeToTerms
    }
    return apiClient.post('/register', payload, {
      withCredentials: true
    })
  },

  login(credentials) {
    return apiClient.post('/login', credentials, {
      withCredentials: true
    })
  }
}

/* ===============================
   Utilisateurs
   =============================== */

// Créer un utilisateur
export const creerUtilisateur = (utilisateur) => {
 const payload = {
  nom: nouvelUtilisateur.value.nom,           // ← important
  email: nouvelUtilisateur.value.email,
  motdepasse: nouvelUtilisateur.value.mot_de_passe,
  role: nouvelUtilisateur.value.role
}


  return apiClient.post('/utilisateurs', payload, {
    withCredentials: true
  })
}

// Récupérer tous les utilisateurs
export const getUtilisateurs = () => {
  return apiClient.get('/api/utilisateurs')
}

export default apiClient
