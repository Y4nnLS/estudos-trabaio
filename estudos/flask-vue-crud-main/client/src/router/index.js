import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import Jogos from '../components/Jogos.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Jogos',
      component: Jogos,
    },
    {
      path: '/ping',
      name: 'ping',
      component: Ping
    },
  ]
})

export default router
