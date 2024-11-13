<template>
  <div>
    <h2>Add New Product</h2>
    <form @submit.prevent="addProduct">
      <label for="name">Name:</label>
      <input type="text" v-model="name" required /><br><br>

      <label for="description">Description:</label>
      <textarea v-model="description" required></textarea><br><br>

      <label for="price">Price:</label>
      <input type="number" v-model="price" required /><br><br>

      <label for="category">Category:</label>
      <input type="text" v-model="category" required /><br><br>

      <label for="stock">Stock:</label>
      <input type="number" v-model="stock" /><br><br>

      <label for="gender">Gender:</label>
      <select v-model="gender" required>
        <option value="male">Male</option>
        <option value="female">Female</option>
      </select>
      <br><br>

      <label for="image_url">Image URL:</label>
      <input type="text" v-model="image_url" /><br><br>

      <label for="tags">Tags (comma separated):</label>
      <input type="text" v-model="tags" /><br><br>

      <button type="submit">Add Product</button>
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
        this.message = 'You must be logged in to add products!';
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
        const response = await axios.post('http://localhost:5000/add_product', productData, {
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
