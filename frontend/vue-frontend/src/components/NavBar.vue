<template>
  <nav class="navbar">
    <div class="navbar-left">
      <router-link to="/">
        <h1 class="navbar-title">Sklep odzieżowy</h1>
      </router-link>
    </div>
    <div class="navbar-center">
      <div class="categories">
        <div v-for="category in categories" :key="category" class="dropdown">
          <router-link :to="'/category/' + category">
            <button>{{ category }}</button>
          </router-link>
        </div>
      </div>
      <div v-if="isLoggedIn">
        <router-link to="/cart">
          <button>Koszyk ({{ cartCount }})</button>
        </router-link>
        <div v-if="isAdmin">
          <router-link to="/add_product">
            <button>Dodaj produkty</button>
          </router-link>
        </div>
      </div>
    </div>
    <div class="navbar-right">
      <div v-if="isLoggedIn">
        <button @click="logout">Wyloguj się</button>
      </div>
      <div v-else>
        <router-link to="/login">Logowanie</router-link> |
        <router-link to="/register">Rejestracja</router-link>
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
      categories: [], // Kategorie produktów
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
  },
  methods: {
    async checkLogin() {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await axios.get('http://localhost:5000/check_login', {
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
          const response = await axios.get('http://localhost:5000/cart', {
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
        const response = await axios.get('http://localhost:5000/products_by_category');
        this.categories = response.data; // Bezpośrednio przypisz dane odpowiedzi
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
      this.$router.push('/'); // Przeniesienie na stronę główną po wylogowaniu
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
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
}

.navbar-left h1 {
  margin: 0;
}

.navbar-center {
  display: flex;
  gap: 15px;
}

.categories {
  display: flex;
  gap: 10px;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

button {
  margin: 5px;
  padding: 10px 15px;
  background-color: #ffffff;
  color: #4caf50;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #eeeeee;
}

p {
  margin: 0;
  font-size: 1rem;
}
</style>
