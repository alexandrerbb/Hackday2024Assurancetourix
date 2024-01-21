import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import HomeView from '@/views/HomeView.vue'
import TicketView from '@/views/TicketView.vue'
import NewTicketView from '@/views/NewTicketView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/new', name: 'new_ticket', component: NewTicketView },
    { path: '/ticket/:id', name: 'ticket', component: TicketView, props: true }
  ]
})

export default router
