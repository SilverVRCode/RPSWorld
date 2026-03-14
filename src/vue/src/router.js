import { createMemoryHistory, createRouter } from 'vue-router'

import AboutView from './pages/AboutView.vue'
import HomeView from './pages/HomeView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/about', component: AboutView },
]

export const router = createRouter({
  history: createMemoryHistory(),
  routes,
})
