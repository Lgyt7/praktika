<template>
  <div id="app">
    <nav v-if="isAuthenticated" class="main-nav">
      <div class="nav-brand">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 18V5l12-2v13"></path>
          <circle cx="6" cy="18" r="3"></circle>
          <circle cx="18" cy="16" r="3"></circle>
        </svg>
        <span>IndieSound</span>
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 18V5l12-2v13"></path>
            <circle cx="6" cy="18" r="3"></circle>
            <circle cx="18" cy="16" r="3"></circle>
          </svg>
          Треки
        </router-link>
        <router-link to="/playlists" class="nav-link">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="9" y1="3" x2="9" y2="21"></line>
          </svg>
          Плейлисты
        </router-link>
      </div>
      <div class="nav-user">
        <span class="user-email">{{ userName }}</span>
        <button @click="logout" class="btn-logout-nav" title="Выйти">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
        </button>
      </div>
    </nav>
    
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const userName = ref('')

const isAuthenticated = computed(() => !!localStorage.getItem('token'))

const fetchUser = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    userName.value = ''
    return
  }
  try {
    // Декодируем JWT токен для получения email
    const payload = JSON.parse(atob(token.split('.')[1]))
    userName.value = payload.sub || 'Пользователь'
  } catch (err) {
    userName.value = 'Пользователь'
  }
}

const logout = () => {
  localStorage.removeItem('token')
  userName.value = ''
  router.push('/login')
}

onMounted(() => {
  fetchUser()
})
</script>

<style>
#app {
  min-height: 100vh;
}

.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: var(--background-card);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.3rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-links {
  display: flex;
  gap: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--border-radius);
  transition: background 0.2s, color 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active {
  background: rgba(99, 102, 241, 0.1);
  color: var(--primary-color);
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-email {
  color: var(--text-secondary);
  font-size: 0.9rem;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-logout-nav {
  background: rgba(239, 68, 68, 0.15);
  border: none;
  color: #ef4444;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
  flex-shrink: 0;
}

.btn-logout-nav svg {
  stroke: #ef4444;
}

.btn-logout-nav:hover {
  background: rgba(239, 68, 68, 0.25);
  transform: scale(1.05);
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
}

@media (max-width: 768px) {
  .main-nav {
    flex-wrap: wrap;
    gap: 12px;
  }

  .nav-links {
    width: 100%;
    justify-content: center;
  }

  .nav-brand {
    margin-right: auto;
  }
}
</style>
