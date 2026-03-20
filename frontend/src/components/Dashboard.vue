<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h2>
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 12px;">
          <path d="M9 18V5l12-2v13"></path>
          <circle cx="6" cy="18" r="3"></circle>
          <circle cx="18" cy="16" r="3"></circle>
        </svg>
        Список треков
      </h2>
      <div class="header-actions">
        <router-link to="/playlists" class="btn-playlists" v-if="isAuthenticated">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="9" y1="3" x2="9" y2="21"></line>
          </svg>
          Плейлисты
        </router-link>
        <button @click="logout" class="btn-logout">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
          Выйти
        </button>
      </div>
    </div>

    <div v-if="tracks.length === 0" class="empty-state">
      <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9 18V5l12-2v13"></path>
        <circle cx="6" cy="18" r="3"></circle>
        <circle cx="18" cy="16" r="3"></circle>
      </svg>
      <p>Треков пока нет</p>
      <span>Будьте первым, кто загрузит свой трек!</span>
    </div>

    <ul v-else class="tracks-list">
      <li v-for="track in tracks" :key="track.id" class="track-card">
        <div class="track-info">
          <div class="track-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
              <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
            </svg>
          </div>
          <div class="track-details">
            <b>{{ track.title }}</b>
            <span class="track-duration">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
              {{ track.duration }}
            </span>
          </div>
        </div>
        <span class="status-badge" :class="getStatusClass(track.status)">
          {{ getStatusText(track.status) }}
        </span>
      </li>
    </ul>

    <div v-if="isAuthenticated" class="upload-section">
      <div class="upload-card">
        <div class="upload-header">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
          </svg>
          <h3>Добавить новый трек</h3>
        </div>
        
        <form @submit.prevent="addTrack">
          <div class="form-row">
            <div class="form-group form-group-wide">
              <label for="title">Название трека</label>
              <input
                id="title"
                v-model="newTrack.title"
                placeholder="Например: Summer Vibes"
                required
              />
            </div>

            <div class="form-group form-group-narrow">
              <label for="duration">Длительность</label>
              <input
                id="duration"
                v-model="newTrack.duration"
                placeholder="3:45"
                required
              />
            </div>
          </div>
          
          <button type="submit" class="btn-upload">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17 8 12 3 7 8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            Загрузить трек
          </button>
        </form>
      </div>
    </div>
    
    <div v-else class="login-prompt">
      <div class="prompt-card">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
        <p>Войдите или зарегистрируйтесь, чтобы загружать свои треки</p>
        <div class="auth-buttons">
          <router-link to="/login" class="btn-login">Войти</router-link>
          <router-link to="/login?register=true" class="btn-register">Регистрация</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const tracks = ref([])
const isAuthenticated = ref(!!localStorage.getItem('token'))
const newTrack = ref({ title: '', duration: '' })
const router = useRouter()

const getStatusClass = (status) => {
  return `status-${status}`
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': 'На проверке',
    'approved': 'Одобрено',
    'rejected': 'Отклонено'
  }
  return statusMap[status] || status
}

const fetchTracks = async () => {
  try {
    const response = await axios.get('http://localhost:8000/tracks/')
    tracks.value = response.data
  } catch (err) {
    console.error('Error fetching tracks:', err)
  }
}

const addTrack = async () => {
  const token = localStorage.getItem('token')
  try {
    await axios.post('http://localhost:8000/tracks/', newTrack.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    newTrack.value = { title: '', duration: '' }
    fetchTracks()
  } catch (err) {
    console.error('Error adding track:', err)
  }
}

const logout = () => {
  localStorage.removeItem('token')
  isAuthenticated.value = false
  router.push('/login')
}

onMounted(() => {
  fetchTracks()
})
</script>

<style scoped>
.dashboard {
  padding: 20px 0;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.dashboard-header h2 {
  display: flex;
  align-items: center;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.btn-playlists {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border-radius: var(--border-radius);
  text-decoration: none;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-playlists:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}

.btn-logout {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.btn-logout:hover {
  background: rgba(239, 68, 68, 0.2);
  box-shadow: 0 10px 30px rgba(239, 68, 68, 0.3);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-secondary);
}

.empty-state svg {
  opacity: 0.3;
  margin-bottom: 24px;
}

.empty-state p {
  font-size: 1.3rem;
  margin-bottom: 8px;
  color: var(--text-primary);
}

/* Tracks List */
.tracks-list {
  display: grid;
  gap: 16px;
  margin-bottom: 40px;
}

.track-card {
  background: var(--background-card);
  padding: 20px 24px;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid rgba(255, 255, 255, 0.05);
  min-width: 0;
}

.track-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 50px rgba(99, 102, 241, 0.15);
}

.track-info {
  display: flex;
  align-items: center;
  gap: 16px;
  min-width: 0;
  flex: 1;
}

.track-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.track-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
  flex: 1;
}

.track-details b {
  font-size: 1.1rem;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-duration {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  color: var(--text-secondary);
  white-space: nowrap;
  flex-shrink: 0;
}

/* Status Badge */
.status-badge {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-pending {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

.status-approved {
  background: rgba(16, 185, 129, 0.15);
  color: var(--success);
}

.status-rejected {
  background: rgba(239, 68, 68, 0.15);
  color: var(--error);
}

/* Upload Section */
.upload-section {
  margin-top: 40px;
}

.upload-card {
  background: var(--background-card);
  padding: 32px;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.upload-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  color: var(--primary-color);
}

.upload-header h3 {
  margin: 0;
  color: var(--text-primary);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 16px;
  align-items: end;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group-wide {
  flex: 1;
  min-width: 0;
}

.form-group-narrow {
  width: 120px;
  flex-shrink: 0;
}

.form-group label {
  font-size: 0.9rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.btn-upload {
  width: 100%;
  margin-top: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

/* Login Prompt */
.login-prompt {
  margin-top: 40px;
}

.prompt-card {
  background: var(--background-card);
  padding: 48px 32px;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.prompt-card svg {
  color: var(--primary-color);
  margin-bottom: 20px;
  opacity: 0.8;
}

.prompt-card p {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.auth-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-login {
  display: inline-block;
  padding: 14px 32px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border-radius: var(--border-radius);
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-login:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}

.btn-register {
  display: inline-block;
  padding: 14px 32px;
  background: transparent;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
  border-radius: var(--border-radius);
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s, background 0.2s;
}

.btn-register:hover {
  transform: translateY(-2px);
  background: rgba(99, 102, 241, 0.1);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.2);
}

/* Responsive */
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .btn-logout {
    align-self: flex-end;
  }

  .track-card {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }

  .track-info {
    flex-direction: column;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
