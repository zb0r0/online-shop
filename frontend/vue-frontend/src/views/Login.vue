<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="login">
      <label for="username">Nazwa użytkownika:</label>
      <input type="text" v-model="username" required /><br><br>
      <label for="password">Hasło:</label>
      <input type="password" v-model="password" required /><br><br>
      <button type="submit">Login</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      message: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:5000/login', {
          username: this.username,
          password: this.password
        });
        this.message = response.data.message;
        localStorage.setItem('token', response.data.token);
        this.$router.push('/');
      } catch (error) {
        if (error.response && error.response.data) {
          this.message = error.response.data.message;
        } else {
          this.message = 'Wystąpił error';
        }
      }
    }
  }
};
</script>
