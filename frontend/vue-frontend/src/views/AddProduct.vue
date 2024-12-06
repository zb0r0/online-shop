<template>
  <div>
    <h2>Dodawanie produktów</h2>
    <form @submit.prevent="addProduct">
      <label for="name">Nazwa:</label>
      <input type="text" v-model="name" required /><br><br>

      <label for="description">Opis:</label>
      <textarea v-model="description" required></textarea><br><br>

      <label for="price">Cena:</label>
      <input type="number" v-model="price" required /><br><br>

      <label for="category">Kategoria:</label>
      <input type="text" v-model="category" required /><br><br>

      <label for="stock">Ilość:</label>
      <input type="number" v-model="stock" /><br><br>

      <label for="gender">Płeć:</label>
      <select v-model="gender" required>
        <option value="male">Mężczyzna</option>
        <option value="female">Kobieta</option>
      </select>
      <br><br>

      <label for="image_url">URL zdjęcia:</label>
      <input type="text" v-model="image_url" /><br><br>

      <label for="tags">Tagi (po przecinku):</label>
      <input type="text" v-model="tags" /><br><br>

      <button type="submit">Dodaj produkt</button>
    </form>

    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AddProductPage',
  data() {
    return {
      name: '',
      description: '',
      price: '',
      category: '',
      stock: 0,
      gender: '',  // Dodajemy nową zmienną
      image_url: '',
      tags: '',
      message: ''
    };
  },
  methods: {
    async addProduct() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.message = 'Musisz być zalogowany, żeby dodać produkt!';
        return;
      }

      const productData = {
        name: this.name,
        description: this.description,
        price: this.price,
        category: this.category,
        stock: this.stock,
        gender: this.gender,  // Przekazujemy gender
        image_url: this.image_url,
        tags: this.tags.split(',').map(tag => tag.trim())
      };

      try {
        const response = await axios.post('${process.env.VUE_APP_API_URL}/add_product', productData, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.message = response.data.message;
      } catch (error) {
        this.message = error.response?.data?.message || 'An error occurred';
      }
    }
  }
};
</script>

<style scoped>
/* Dodaj własne style */
</style>
