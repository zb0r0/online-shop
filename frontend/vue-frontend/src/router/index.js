import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/Home.vue';
import LoginPage from '@/views/Login.vue';
import RegisterPage from '@/views/Register.vue';
import AddProductPage from '@/views/AddProduct.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/add_product', component: AddProductPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
