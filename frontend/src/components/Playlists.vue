<template>
  <div class="playlists-page">
    <div class="page-header">
      <h2>
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 12px;">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="9" y1="3" x2="9" y2="21"></line>
        </svg>
        Мои плейлисты
      </h2>
      <button @click="showCreateModal = true" class="btn-create">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        Создать плейлист
      </button>
    </div>

    <div v-if="playlists.length === 0" class="empty-state">
      <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
        <line x1="9" y1="3" x2="9" y2="21"></line>
      </svg>
      <p>У вас пока нет плейлистов</p>
      <span>Создайте свой первый плейлист!</span>
    </div>

    <div v-else class="playlists-grid">
      <div v-for="playlist in playlists" :key="playlist.id" class="playlist-card" @click="selectPlaylist(playlist)">
        <div class="playlist-cover">
          <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 18V5l12-2v13"></path>
            <circle cx="6" cy="18" r="3"></circle>
            <circle cx="18" cy="16" r="3"></circle>
          </svg>
        </div>
        <div class="playlist-info">
          <h3>{{ playlist.title }}</h3>
          <span class="playlist-count">{{ playlist.tracks.length }} треков</span>
        </div>
        <button class="btn-delete-playlist" @click.stop="deletePlaylist(playlist.id)">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
        </button>
      </div>
    </div>

    <!-- Playlist Detail Modal -->
    <div v-if="selectedPlaylist" class="modal-overlay" @click="selectedPlaylist = null">
      <div class="modal-content playlist-detail" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedPlaylist.title }}</h3>
          <button class="close-btn" @click="selectedPlaylist = null">&times;</button>
        </div>
        
        <div v-if="selectedPlaylist.tracks.length === 0" class="empty-tracks">
          <p>В этом плейлисте пока нет треков</p>
        </div>
        
        <ul v-else class="playlist-tracks-list">
          <li v-for="track in selectedPlaylist.tracks" :key="track.id" class="playlist-track-item">
            <div class="track-info">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
              </svg>
              <div>
                <b>{{ track.title }}</b>
                <span class="duration">{{ track.duration }}</span>
              </div>
            </div>
            <button class="btn-remove-track" @click="removeTrackFromPlaylist(track.id)">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </li>
        </ul>
        
        <div class="add-track-section">
          <h4>Добавить трек</h4>
          <select v-model="selectedTrackId" class="track-select">
            <option value="" disabled>Выберите трек</option>
            <option v-for="track in availableTracks" :key="track.id" :value="track.id">
              {{ track.title }} ({{ track.duration }})
            </option>
          </select>
          <button @click="addTrackToPlaylist" class="btn-add-track" :disabled="!selectedTrackId">Добавить</button>
        </div>
      </div>
    </div>

    <!-- Create Playlist Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
      <div class="modal-content create-playlist" @click.stop>
        <div class="modal-header">
          <h3>Новый плейлист</h3>
          <button class="close-btn" @click="showCreateModal = false">&times;</button>
        </div>
        
        <form @submit.prevent="createPlaylist">
          <div class="form-group">
            <label for="playlist-title">Название</label>
            <input 
              id="playlist-title"
              v-model="newPlaylist.title" 
              type="text" 
              placeholder="Например: Мои любимые треки" 
              required 
            />
          </div>
          <button type="submit" class="btn-primary">Создать</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const playlists = ref([])
const allTracks = ref([])
const selectedPlaylist = ref(null)
const selectedTrackId = ref(null)
const showCreateModal = ref(false)
const newPlaylist = ref({ title: '' })
const router = useRouter()

const availableTracks = computed(() => {
  if (!selectedPlaylist.value) return []
  const playlistTrackIds = selectedPlaylist.value.tracks.map(t => t.id)
  return allTracks.value.filter(t => !playlistTrackIds.includes(t.id))
})

const fetchPlaylists = async () => {
  const token = localStorage.getItem('token')
  try {
    const response = await axios.get('http://localhost:8000/playlists/my', {
      headers: { Authorization: `Bearer ${token}` }
    })
    playlists.value = response.data
  } catch (err) {
    console.error('Error fetching playlists:', err)
  }
}

const fetchTracks = async () => {
  try {
    const response = await axios.get('http://localhost:8000/tracks/')
    allTracks.value = response.data
  } catch (err) {
    console.error('Error fetching tracks:', err)
  }
}

const createPlaylist = async () => {
  const token = localStorage.getItem('token')
  try {
    const response = await axios.post('http://localhost:8000/playlists/', newPlaylist.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    playlists.value.push(response.data)
    newPlaylist.value = { title: '' }
    showCreateModal.value = false
  } catch (err) {
    console.error('Error creating playlist:', err)
  }
}

const selectPlaylist = async (playlist) => {
  const token = localStorage.getItem('token')
  try {
    const response = await axios.get(`http://localhost:8000/playlists/${playlist.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    selectedPlaylist.value = response.data
    selectedTrackId.value = null
  } catch (err) {
    console.error('Error fetching playlist:', err)
  }
}

const addTrackToPlaylist = async () => {
  if (!selectedTrackId.value || !selectedPlaylist.value) return
  const token = localStorage.getItem('token')
  try {
    const response = await axios.post(
      `http://localhost:8000/playlists/${selectedPlaylist.value.id}/tracks`,
      { track_id: selectedTrackId.value },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    selectedPlaylist.value = response.data
    const index = playlists.value.findIndex(p => p.id === selectedPlaylist.value.id)
    if (index !== -1) {
      playlists.value[index] = response.data
    }
    selectedTrackId.value = null
  } catch (err) {
    console.error('Error adding track:', err)
  }
}

const removeTrackFromPlaylist = async (trackId) => {
  if (!selectedPlaylist.value) return
  const token = localStorage.getItem('token')
  try {
    const response = await axios.delete(
      `http://localhost:8000/playlists/${selectedPlaylist.value.id}/tracks/${trackId}`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    selectedPlaylist.value = response.data
    const index = playlists.value.findIndex(p => p.id === selectedPlaylist.value.id)
    if (index !== -1) {
      playlists.value[index] = response.data
    }
  } catch (err) {
    console.error('Error removing track:', err)
  }
}

const deletePlaylist = async (playlistId) => {
  if (!confirm('Вы уверены, что хотите удалить этот плейлист?')) return
  const token = localStorage.getItem('token')
  try {
    await axios.delete(`http://localhost:8000/playlists/${playlistId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    playlists.value = playlists.value.filter(p => p.id !== playlistId)
  } catch (err) {
    console.error('Error deleting playlist:', err)
  }
}

onMounted(() => {
  fetchPlaylists()
  fetchTracks()
})
</script>

<style scoped>
.playlists-page {
  padding: 20px 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.page-header h2 {
  display: flex;
  align-items: center;
  margin: 0;
}

.btn-create {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-create:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
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

/* Playlists Grid */
.playlists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.playlist-card {
  background: var(--background-card);
  padding: 24px;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid rgba(255, 255, 255, 0.05);
  position: relative;
}

.playlist-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 15px 50px rgba(99, 102, 241, 0.2);
}

.playlist-cover {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: 16px;
}

.playlist-info h3 {
  font-size: 1.1rem;
  margin: 0 0 8px 0;
  color: var(--text-primary);
}

.playlist-count {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.btn-delete-playlist {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(239, 68, 68, 0.2);
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s, background 0.2s, transform 0.2s;
  flex-shrink: 0;
}

.btn-delete-playlist svg {
  stroke: #ef4444;
  stroke-width: 2;
}

.playlist-card:hover .btn-delete-playlist {
  opacity: 1;
}

.btn-delete-playlist:hover {
  background: rgba(239, 68, 68, 0.3);
  transform: scale(1.05);
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
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.playlist-detail {
  max-width: 600px;
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

/* Playlist Tracks List */
.empty-tracks {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-secondary);
}

.playlist-tracks-list {
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
}

.playlist-track-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--background-input);
  border-radius: 8px;
  margin-bottom: 8px;
}

.playlist-track-item .track-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.playlist-track-item .track-info svg {
  color: var(--primary-color);
}

.playlist-track-item b {
  display: block;
  color: var(--text-primary);
}

.playlist-track-item .duration {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.btn-remove-track {
  background: rgba(239, 68, 68, 0.2);
  border: none;
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

.btn-remove-track svg {
  stroke: #ef4444;
  stroke-width: 2;
}

.btn-remove-track:hover {
  background: rgba(239, 68, 68, 0.3);
  transform: scale(1.05);
}

/* Add Track Section */
.add-track-section {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 24px;
}

.add-track-section h4 {
  margin: 0 0 12px 0;
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.track-select {
  width: 100%;
  padding: 12px 16px;
  background: var(--background-input);
  border: 2px solid transparent;
  border-radius: var(--border-radius);
  color: var(--text-primary);
  font-size: 1rem;
  margin-bottom: 12px;
  cursor: pointer;
}

.track-select:focus {
  outline: none;
  border-color: var(--primary-color);
}

.btn-add-track {
  width: 100%;
  padding: 12px 24px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s, opacity 0.2s;
}

.btn-add-track:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-add-track:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}

/* Create Playlist Form */
.create-playlist form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.create-playlist .form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.create-playlist label {
  font-size: 0.9rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.create-playlist input {
  padding: 14px 18px;
  border: 2px solid transparent;
  border-radius: var(--border-radius);
  background: var(--background-input);
  color: var(--text-primary);
  font-size: 1rem;
}

.create-playlist input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.btn-primary {
  padding: 14px 24px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .btn-create {
    width: 100%;
    justify-content: center;
  }

  .playlists-grid {
    grid-template-columns: 1fr;
  }
}
</style>
