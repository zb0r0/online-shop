<template>
  <div>
    <h1>Welcome to Our Site</h1>
    <div v-if="isLoggedIn">
      <p>Welcome back, {{ username }}</p>
      <button @click="logout">Logout</button>
      <div v-if="isAdmin">
        <router-link to="/add_product">
          <button>Add Product</button>
        </router-link>
      </div>
    </div>
    <div v-else>
      <router-link to="/login">Login</router-link> |
      <router-link to="/register">Register</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomePage',
  data() {
    return {
      isLoggedIn: false,
      isAdmin: false,
      username: ''
    };
  },
  mounted() {
    this.checkLogin();
  },
  methods: {
    async checkLogin() {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await axios.get('http://localhost:5000/check_login', {
            headers: { Authorization: `Bearer ${token}` }
          });
          this.isLoggedIn = true;
          this.username = response.data.message.split(',')[1].trim();
          this.isAdmin = response.data.message.includes('permissions: 1');
        } catch (error) {
          console.log('Not logged in');
        }
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.isLoggedIn = false;
      this.username = '';
      this.isAdmin = false;
    }
  }
};
</script>
