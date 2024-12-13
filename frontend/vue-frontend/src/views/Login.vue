<template>
  <div class="login-container">
    <h2 class="login-title">Logowanie</h2>
    <form @submit.prevent="login" class="login-form">
      <div class="form-group">
        <label for="username">Nazwa użytkownika:</label>
        <input type="text" v-model="username" id="username" required />
      </div>

      <div class="form-group">
        <label for="password">Hasło:</label>
        <input type="password" v-model="password" id="password" required />
      </div>

      <button type="submit" class="submit-button">Zaloguj się</button>
    </form>

    <p v-if="message" class="message">{{ message }}</p>
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

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.login-title {
  font-size: 1.8rem;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-size: 1rem;
  color: #333;
  margin-bottom: 5px;
}

input {
  font-size: 1rem;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  outline: none;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #2196f3;
}

.submit-button {
  background-color: #4caf50;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #45a049;
}

.message {
  text-align: center;
  font-size: 1rem;
  color: #f44336;
  margin-top: 15px;
}
</style>
