<template>
  <nav class="navbar">
    <div class="navbar-left">
      <router-link to="/" class="navbar-title">
        Sklep odzieżowy
      </router-link>
    </div>
    <div class="navbar-center">
      <div class="categories">
        <div v-for="category in categories" :key="category" class="dropdown">
          <router-link :to="'/category/' + category" class="category-link">
            {{ category }}
          </router-link>
        </div>
      </div>
      <div v-if="isLoggedIn" class="cart-container">
        <router-link to="/cart" class="cart-link">
          Koszyk ({{ cartCount }})
        </router-link>
      </div>
    </div>
    <div class="navbar-right">
      <div v-if="isAdmin" class="admin-container">
        <router-link to="/add_product" class="category-link">
          Dodaj produkty
        </router-link>
        <router-link to="/analysis" class="category-link">
          Analiza
        </router-link>
      </div>
      <div v-if="isLoggedIn" class="logged-in-container">
        <router-link to="/my-orders" class="category-link">Moje zamówienia</router-link>
        <button class="navbar-button logout-button" @click="logout">Wyloguj się</button>
      </div>
      <div v-else>
        <router-link to="/login" class="auth-link">Logowanie</router-link>
        |
        <router-link to="/register" class="auth-link">Rejestracja</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
import axios from 'axios';

export default {
  name: 'NavBar',
  data() {
    return {
      isLoggedIn: false,
      isAdmin: false,
      username: '',
      cart: [],
      categories: [],
    };
  },
  computed: {
    cartCount() {
      return this.cart.reduce((count, item) => count + item.quantity, 0);
    },
  },
  mounted() {
    this.checkLogin();
    this.fetchCart();
    this.fetchCategories();
    setInterval(() => {
      this.fetchCart();
    }, 5000); // Odświeżaj dane koszyka co 5 sekund
  },
  methods: {
    async checkLogin() {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await axios.get('http://48.209.24.37:5000/check_login', {
            headers: { Authorization: `Bearer ${token}` },
          });
          this.isLoggedIn = true;
          this.username = response.data.message.split(',')[1].trim();
          this.isAdmin = response.data.message.includes('permissions: 1');
        } catch (error) {
          console.log('Not logged in');
        }
      }
    },
    async fetchCart() {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await axios.get('http://48.209.24.37:5000/cart', {
            headers: { Authorization: `Bearer ${token}` },
          });
          this.cart = response.data.cart;
        } catch (error) {
          console.log('Error fetching cart');
        }
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get('http://48.209.24.37:5000/products_by_category');
        this.categories = response.data;
      } catch (error) {
        console.log('Error fetching categories:', error);
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.isLoggedIn = false;
      this.username = '';
      this.isAdmin = false;
      this.cart = [];
      this.$router.push('/');
    },
  },
  watch: {
    async $route() {
      await this.checkLogin();
      await this.fetchCart();
    },
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #282c34;
  color: #ffffff;
  padding: 10px 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.navbar-title {
  color: #61dafb;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
}

.navbar-center {
  display: flex;
  gap: 20px;
}

.categories {
  display: flex;
  gap: 15px;
}

.category-link {
  text-decoration: none;
  color: #ffffff;
  background-color: #2196f3;
  padding: 5px 10px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.category-link:hover {
  background-color: #1e88e5;
}

.cart-container {
  display: flex;
  align-items: center;
}

.cart-link {
  color: #ffffff;
  text-decoration: none;
  font-weight: bold;
}

.navbar-right {
  display: flex;
  gap: 15px;
  align-items: center;
}

.admin-container {
  display: flex;
  gap: 10px;
}

.logged-in-container {
  display: flex;
  gap: 10px;
  align-items: center;
}

.navbar-button {
  color: #ffffff;
  background-color: #4caf50;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.navbar-button:hover {
  background-color: #45a049;
}

.auth-link {
  color: #ffffff;
  text-decoration: none;
}

.logout-button {
  background-color: #f44336;
}

.logout-button:hover {
  background-color: #d32f2f;
}
</style>
