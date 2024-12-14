<template>
  <div class="register-container">
    <h2 class="register-title">Rejestracja</h2>
    <form @submit.prevent="register" class="register-form">
      <div class="form-group">
        <label for="username">Nazwa użytkownika:</label>
        <input type="text" v-model="username" id="username" required />
      </div>

      <div class="form-group">
        <label for="password">Hasło:</label>
        <input type="password" v-model="password" id="password" required />
      </div>

      <div class="form-group">
        <label for="birthdate">Data urodzenia:</label>
        <input type="date" v-model="birthdate" id="birthdate" required />
      </div>

      <div class="form-group">
        <label for="gender">Płeć:</label>
        <select v-model="gender" id="gender" required>
          <option value="Male">Mężczyzna</option>
          <option value="Female">Kobieta</option>
        </select>
      </div>

      <div class="form-group">
        <label for="location">Lokalizacja:</label>
        <select v-model="location" id="location" required>
          <option value="Dolnośląskie">Dolnośląskie</option>
          <option value="Kujawsko-Pomorskie">Kujawsko-Pomorskie</option>
          <option value="Lubelskie">Lubelskie</option>
          <option value="Lubuskie">Lubuskie</option>
          <option value="Łódzkie">Łódzkie</option>
          <option value="Małopolskie">Małopolskie</option>
          <option value="Mazowieckie">Mazowieckie</option>
          <option value="Opolskie">Opolskie</option>
          <option value="Podkarpackie">Podkarpackie</option>
          <option value="Podlaskie">Podlaskie</option>
          <option value="Pomorskie">Pomorskie</option>
          <option value="Śląskie">Śląskie</option>
          <option value="Świętokrzyskie">Świętokrzyskie</option>
          <option value="Warmińsko-Mazurskie">Warmińsko-Mazurskie</option>
          <option value="Wielkopolskie">Wielkopolskie</option>
          <option value="Zachodniopomorskie">Zachodniopomorskie</option>
        </select>
      </div>

      <button type="submit" class="submit-button">Załóż konto</button>
    </form>

    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterPage',
  data() {
    return {
      username: '',
      password: '',
      birthdate: '',
      gender: '',
      location: '',
      message: ''
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://48.209.24.37:5000/register', {
          username: this.username,
          password: this.password,
          birthdate: this.birthdate,
          gender: this.gender,
          location: this.location,
          permissions: 0
        });
        this.message = response.data.message;
      } catch (error) {
        if (error.response && error.response.data) {
          this.message = error.response.data.message;
        } else {
          this.message = 'An error occurred';
        }
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.register-title {
  font-size: 1.8rem;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.register-form {
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

input, select {
  font-size: 1rem;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  outline: none;
  transition: border-color 0.3s;
}

input:focus, select:focus {
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
