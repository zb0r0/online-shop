<template>
  <div>
    <header>
      <h1>Sklep odzieżowy</h1>
      <div v-if="isLoggedIn">
        <p>Cześć, {{ username }}</p>
        <button @click="logout">Wyloguj się</button>
        <router-link to="/cart">
          <button>Koszyk ({{ cartCount }})</button>
        </router-link>
        <div v-if="isAdmin">
          <router-link to="/add_product">
            <button>Dodaj produkty</button>
          </router-link>
        </div>
      </div>
      <div v-else>
        <router-link to="/login">Logowanie</router-link> |
        <router-link to="/register">Rejestracja</router-link>
      </div>
    </header>
    <main>
      <ProductGrid />
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import ProductGrid from '@/views/ProductGrid.vue';

export default {
  name: 'HomePage',
  data() {
    return {
      isLoggedIn: false,
      isAdmin: false,
      username: '',
      cart: [],
    };
  },
  components: {
    ProductGrid,
  },
  computed: {
    cartCount() {
      return this.cart.reduce((count, item) => count + item.quantity, 0);
    },
  },
  mounted() {
    this.checkLogin();
    this.fetchCart();
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
    logout() {
      localStorage.removeItem('token');
      this.isLoggedIn = false;
      this.username = '';
      this.isAdmin = false;
      this.cart = [];  // Clear cart when logged out
    },
  },
};
</script>

<style scoped>
header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

header div {
  margin: 10px 0;
}

button {
  margin: 5px;
  padding: 10px 15px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

main {
  width: 100%;
  display: flex;
  justify-content: center;
}
</style>
