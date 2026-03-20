import { createRouter, createWebHistory } from 'vue-router'
import Login from './components/Login.vue'
import Dashboard from './components/Dashboard.vue'
import Playlists from './components/Playlists.vue'

const routes = [
  { path: '/', component: Dashboard },
  { path: '/login', component: Login },
  { path: '/playlists', component: Playlists, meta: { requiresAuth: true } }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
