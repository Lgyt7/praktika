<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="icon-wrapper">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        <h2>Вход в систему</h2>
        <p class="subtitle">Введите свои данные для продолжения</p>
      </div>
      
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            id="email"
            v-model="email" 
            type="email" 
            placeholder="your@email.com" 
            required 
          />
        </div>
        
        <div class="form-group">
          <label for="password">Пароль</label>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            placeholder="••••••••" 
            required 
          />
        </div>
        
        <button type="submit" class="btn-primary">
          <span>Войти</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"></line>
            <polyline points="12 5 19 12 12 19"></polyline>
          </svg>
        </button>
      </form>
      
      <p v-if="error" class="error-message">{{ error }}</p>
      
      <div class="login-footer">
        <p>Нет аккаунта? <a href="#" @click.prevent="showRegister = true">Зарегистрироваться</a></p>
      </div>
    </div>
    
    <!-- Registration Modal -->
    <div v-if="showRegister" class="modal-overlay" @click="showRegister = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Регистрация</h3>
          <button class="close-btn" @click="showRegister = false">&times;</button>
        </div>
        
        <form @submit.prevent="register">
          <div class="form-group">
            <label for="reg-name">Имя</label>
            <input 
              id="reg-name"
              v-model="registerData.name" 
              type="text" 
              placeholder="Ваше имя" 
              required 
            />
          </div>
          
          <div class="form-group">
            <label for="reg-email">Email</label>
            <input 
              id="reg-email"
              v-model="registerData.email" 
              type="email" 
              placeholder="your@email.com" 
              required 
            />
          </div>
          
          <div class="form-group">
            <label for="reg-password">Пароль</label>
            <input 
              id="reg-password"
              v-model="registerData.password" 
              type="password" 
              placeholder="••••••••" 
              required 
            />
          </div>
          
          <div class="form-group">
            <label for="reg-role">Роль</label>
            <select id="reg-role" v-model="registerData.role">
              <option value="listener">Слушатель</option>
              <option value="musician">Музыкант</option>
            </select>
          </div>
          
          <button type="submit" class="btn-primary">Зарегистрироваться</button>
        </form>
        
        <p v-if="registerError" class="error-message">{{ registerError }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()
const route = useRoute()
const showRegister = ref(false)
const registerData = ref({ name: '', email: '', password: '', role: 'listener' })
const registerError = ref('')

onMounted(() => {
  if (route.query.register === 'true') {
    showRegister.value = true
  }
})

const login = async () => {
  try {
    const formData = new URLSearchParams()
    formData.append('username', email.value)
    formData.append('password', password.value)

    const response = await axios.post('http://localhost:8000/auth/login', formData)
    localStorage.setItem('token', response.data.access_token)
    router.push('/')
  } catch (err) {
    error.value = 'Неверный email или пароль'
  }
}

const register = async () => {
  try {
    await axios.post('http://localhost:8000/auth/register', registerData.value)
    showRegister.value = false
    error.value = ''
    registerData.value = { name: '', email: '', password: '', role: 'listener' }
    alert('Регистрация успешна! Теперь войдите.')
  } catch (err) {
    registerError.value = err.response?.data?.detail || 'Ошибка регистрации'
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.login-card {
  background: var(--background-card);
  padding: 40px;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  width: 100%;
  max-width: 420px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.icon-wrapper {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.subtitle {
  color: var(--text-secondary);
  margin-top: 8px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-size: 0.9rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.btn-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
}

.login-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-secondary);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: var(--background-card);
  padding: 32px;
  border-radius: var(--border-radius);
  width: 100%;
  max-width: 420px;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.modal-header h3 {
  margin: 0;
  color: var(--text-primary);
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 28px;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: var(--text-primary);
  background: none;
  box-shadow: none;
  transform: none;
}

select {
  padding: 14px 18px;
  border: 2px solid transparent;
  border-radius: var(--border-radius);
  background: var(--background-input);
  color: var(--text-primary);
  font-size: 1rem;
  cursor: pointer;
}

select:focus {
  outline: none;
  border-color: var(--primary-color);
}

select option {
  background: var(--background-card);
  color: var(--text-primary);
}
</style>
