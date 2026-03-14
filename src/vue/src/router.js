import { createRouter } from 'vue-routes'

import { default as AboutView, default as HomeView } from './pages/HomeView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/about', component: AboutView },
]

export const router = createRouter({
  history: createMemoryHistory(),
  routes,
})
