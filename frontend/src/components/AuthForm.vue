<template>
  <div class="auth-container">
    <div class="auth-content">
      <!-- Section gauche avec branding et image -->
      <div class="brand-section">
        <div class="brand-content">
          <div class="logo-container">
            <div class="logo">
              <span class="logo-text">SocialApp</span>
            </div>
          </div>
          <h1 class="brand-title">Connectez-vous avec vos amis</h1>
          <p class="brand-subtitle">
            Partagez vos moments, découvrez du contenu et restez en contact avec les personnes qui comptent pour vous.
          </p>
          <div class="features-list">
            <div class="feature-item">
              <div class="feature-icon">🌟</div>
              <span>Partagez vos moments</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">👥</div>
              <span>Connectez-vous avec vos amis</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">🔒</div>
              <span>Sécurisé et privé</span>
            </div>
          </div>
        </div>
        <div class="hero-image">
          <img src="https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=800" alt="People connecting" />
        </div>
      </div>

      <!-- Section droite avec formulaires -->
      <div class="form-section">
        <div class="form-container">
          <div class="form-header">
            <div class="tab-switcher">
              <!-- Seul bouton Connexion -->
              <button class="tab-btn active">Connexion</button>
              <!-- L'autre bouton est supprimé -->
            </div>
          </div>

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
/* 💡 Ne rien modifier ici, tu peux garder tout ton CSS comme tu l’as fait */
</style>

<style scoped>
.auth-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

.auth-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('https://images.pexels.com/photos/3184339/pexels-photo-3184339.jpeg?auto=compress&cs=tinysrgb&w=1600') center/cover;
  opacity: 0.1;
  z-index: 0;
}

.auth-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  max-width: 1200px;
  width: 100%;
  position: relative;
  z-index: 1;
}

.brand-section {
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: white;
  padding: 2rem;
}

.brand-content {
  margin-bottom: 3rem;
}

.logo-container {
  margin-bottom: 2rem;
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.logo-text {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(45deg, #fff, #f0f8ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-title {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.brand-subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.1rem;
}

.feature-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  backdrop-filter: blur(10px);
}

.hero-image {
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  transform: perspective(1000px) rotateY(-5deg) rotateX(2deg);
  transition: transform 0.3s ease;
}

.hero-image:hover {
  transform: perspective(1000px) rotateY(-2deg) rotateX(1deg) scale(1.02);
}

.hero-image img {
  width: 100%;
  height: 400px;
  object-fit: cover;
  display: block;
}

.form-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
  width: 100%;
  max-width: 450px;
}

.form-header {
  margin-bottom: 2rem;
}

.tab-switcher {
  position: relative;
  display: flex;
  background: #f8f9fa;
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
  color: #6c757d;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.tab-btn.active {
  color: #1877f2;
}

/* On peut garder l'indicateur mais il ne sera pas utilisé ici */
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

.tab-indicator.move-right {
  transform: translateX(100%);
}

.form-wrapper {
  position: relative;
  overflow: hidden;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

@media (max-width: 1024px) {
  .auth-content {
    grid-template-columns: 1fr;
    gap: 2rem;
    text-align: center;
  }
  
  .brand-section {
    order: 2;
  }
  
  .form-section {
    order: 1;
  }
  
  .brand-title {
    font-size: 2.5rem;
  }
  
  .hero-image {
    transform: none;
    max-width: 400px;
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  .auth-container {
    padding: 1rem;
  }
  
  .form-container {
    padding: 2rem;
  }
  
  .brand-title {
    font-size: 2rem;
  }
  
  .brand-subtitle {
    font-size: 1.1rem;
  }
}
</style>
