import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/Home.vue';
import LoginPage from '@/views/Login.vue';
import RegisterPage from '@/views/Register.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
