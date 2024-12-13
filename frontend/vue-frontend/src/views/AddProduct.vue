<template>
  <div class="add-product-container">
    <h2 class="page-title">Dodawanie produktów</h2>
    <form @submit.prevent="addProduct" class="add-product-form">
      <div class="form-group">
        <label for="name">Nazwa:</label>
        <input type="text" v-model="name" id="name" required />
      </div>

      <div class="form-group">
        <label for="description">Opis:</label>
        <textarea v-model="description" id="description" required></textarea>
      </div>

      <div class="form-group">
        <label for="price">Cena:</label>
        <input type="number" v-model="price" id="price" required />
      </div>

      <div class="form-group">
        <label for="category">Kategoria:</label>
        <input type="text" v-model="category" id="category" required />
      </div>

      <div class="form-group">
        <label for="stock">Ilość:</label>
        <input type="number" v-model="stock" id="stock" />
      </div>

      <div class="form-group">
        <label for="gender">Płeć:</label>
        <select v-model="gender" id="gender" required>
          <option value="male">Mężczyzna</option>
          <option value="female">Kobieta</option>
        </select>
      </div>

      <div class="form-group">
        <label for="image_url">URL zdjęcia:</label>
        <input type="text" v-model="image_url" id="image_url" />
      </div>

      <div class="form-group">
        <label for="tags">Tagi (po przecinku):</label>
        <input type="text" v-model="tags" id="tags" />
      </div>

      <button type="submit" class="submit-button">Dodaj produkt</button>
    </form>

    <p v-if="message" class="message">{{ message }}</p>
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
      gender: '',
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
        gender: this.gender,
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
.add-product-container {
  max-width: 600px;
  margin: 0 auto;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.page-title {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: #333;
}

.add-product-form {
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

input, textarea, select {
  font-size: 1rem;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  outline: none;
  transition: border-color 0.3s;
}

input:focus, textarea:focus, select:focus {
  border-color: #2196f3;
}

textarea {
  resize: vertical;
  min-height: 80px;
}

.submit-button {
  background-color: #1e88e5;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #1e88e5;
}

.message {
  text-align: center;
  font-size: 1rem;
  color: #1e88e5;
  margin-top: 15px;
}
</style>
