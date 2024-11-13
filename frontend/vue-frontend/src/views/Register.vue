<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="register">
      <label for="username">Username:</label>
      <input type="text" v-model="username" required /><br><br>

      <label for="password">Password:</label>
      <input type="password" v-model="password" required /><br><br>

      <label for="birthdate">Birthdate:</label>
      <input type="date" v-model="birthdate" required /><br><br>

      <label for="gender">Gender:</label>
      <select v-model="gender" required>
        <option value="Male">Male</option>
        <option value="Female">Female</option>
      </select><br><br>

      <label for="location">Location:</label>
      <select v-model="location" required>
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
      </select><br><br>

      <button type="submit">Register</button>
    </form>
    <p v-if="message">{{ message }}</p>
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
        const response = await axios.post('http://localhost:5000/register', {
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
