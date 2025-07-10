<template>
  <div class="auth-system">
    <!-- Background avec pattern -->
    <div class="auth-background">
      <div class="pattern-overlay"></div>
    </div>

    <div class="auth-container">
      <!-- Section gauche - Branding et informations -->
      <div class="brand-section">
        <div class="brand-content">
          <!-- Logo et titre -->
          <div class="logo-section">
            <div class="logo">
              <div class="logo-icon">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 3v18h18"/>
                  <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/>
                  <circle cx="12" cy="12" r="1"/>
                  <circle cx="19" cy="5" r="2"/>
                </svg>
              </div>
              <span class="logo-text">InsightViz</span>
            </div>
            <p class="tagline">Analyse automatisée des données logistiques</p>
          </div>

          <!-- Features -->
          <div class="features">
            <h3>Transformez vos données en insights</h3>
            <div class="feature-list">
              <div class="feature-item">
                <div class="feature-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                </div>
                <div>
                  <h4>Analyse en temps réel</h4>
                  <p>Visualisez vos KPIs logistiques instantanément</p>
                </div>
              </div>
              <div class="feature-item">
                <div class="feature-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                    <polyline points="3.27,6.96 12,12.01 20.73,6.96"/>
                    <line x1="12" y1="22.08" x2="12" y2="12"/>
                  </svg>
                </div>
                <div>
                  <h4>Rapports automatisés</h4>
                  <p>Génération automatique de rapports détaillés</p>
                </div>
              </div>
              <div class="feature-item">
                <div class="feature-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                  </svg>
                </div>
                <div>
                  <h4>Sécurité avancée</h4>
                  <p>Protection des données avec chiffrement de bout en bout</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Stats -->
          <div class="stats">
            <div class="stat-item">
              <span class="stat-number">500+</span>
              <span class="stat-label">Entreprises</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">2M+</span>
              <span class="stat-label">Données analysées</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">99.9%</span>
              <span class="stat-label">Uptime</span>
            </div>
          </div>
        </div>

        <!-- Image illustration -->
        <div class="illustration">
          <img 
            src="https://images.pexels.com/photos/7688336/pexels-photo-7688336.jpeg?auto=compress&cs=tinysrgb&w=800" 
            alt="Analyse de données logistiques"
          />
        </div>
      </div>

      <!-- Section droite - Formulaire de connexion uniquement -->
      <div class="form-section">
        <div class="form-container">
          <!-- Suppression des onglets -->
          <!-- Formulaire de connexion -->
          <div class="form-wrapper">
            <LoginForm />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import LoginForm from './LoginForm.vue'
</script>

<style scoped>
.auth-system {
  min-height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.auth-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  z-index: 0;
}

.pattern-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 25% 25%, rgba(255,255,255,0.1) 2px, transparent 2px),
    radial-gradient(circle at 75% 75%, rgba(255,255,255,0.1) 2px, transparent 2px);
  background-size: 60px 60px;
  opacity: 0.3;
}

.auth-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  max-width: 1400px;
  width: 100%;
  position: relative;
  z-index: 1;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.brand-section {
  padding: 3rem;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.brand-content {
  flex: 1;
}

.logo-section {
  margin-bottom: 3rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.logo-icon {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.logo-text {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(45deg, #fff, #e0f2fe);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.tagline {
  font-size: 1.1rem;
  opacity: 0.9;
  font-weight: 500;
}

.features h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 2rem;
  opacity: 0.95;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.feature-icon {
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  flex-shrink: 0;
}

.feature-item h4 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.feature-item p {
  font-size: 0.95rem;
  opacity: 0.8;
  line-height: 1.4;
}

.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  padding: 2rem 0;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
  font-weight: 500;
}

.illustration {
  margin-top: 2rem;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
  transform: perspective(1000px) rotateY(-5deg) rotateX(2deg);
  transition: transform 0.3s ease;
}

.illustration:hover {
  transform: perspective(1000px) rotateY(-2deg) rotateX(1deg) scale(1.02);
}

.illustration img {
  width: 100%;
  height: 300px;
  object-fit: cover;
  display: block;
}

.form-section {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-container {
  width: 100%;
  max-width: 420px;
}

.tab-navigation {
  position: relative;
  display: flex;
  background: #f1f5f9;
  border-radius: 16px;
  padding: 6px;
  margin-bottom: 2rem;
}

.tab-btn {
  flex: 1;
  padding: 1rem 1.5rem;
  border: none;
  background: transparent;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.tab-btn.active {
  color: #1e40af;
}

.tab-indicator {
  position: absolute;
  top: 6px;
  left: 6px;
  width: calc(50% - 6px);
  height: calc(100% - 12px);
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
}

.tab-indicator.slide-right {
  transform: translateX(100%);
}

.form-wrapper {
  position: relative;
  overflow: hidden;
}

@media (max-width: 1200px) {
  .auth-container {
    grid-template-columns: 1fr;
    gap: 0;
    max-width: 500px;
  }
  
  .brand-section {
    display: none;
  }
  
  .form-section {
    border-radius: 24px;
  }
}

@media (max-width: 768px) {
  .auth-system {
    padding: 1rem;
  }
  
  .form-section {
    padding: 2rem;
  }
  
  .stats {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>