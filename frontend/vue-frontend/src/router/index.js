import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/Home.vue';
import LoginPage from '@/views/Login.vue';
import RegisterPage from '@/views/Register.vue';
import AddProductPage from '@/views/AddProduct.vue';
import CartPage from '@/views/CartView.vue';
import CheckoutView from '@/views/OrderPage.vue';
import RedirectToHome from '@/views/RedirectToHome.vue';
import ProductDetails from "@/views/ProductDetails";

const routes = [
  { path: '/', component: HomePage },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/add_product', component: AddProductPage },
  { path: '/cart', component: CartPage },
  { path: '/checkout', name: 'OrderPage', component: CheckoutView },
  { path: '/notify', component: RedirectToHome },
  { path: '/product/:id', component: ProductDetails },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
