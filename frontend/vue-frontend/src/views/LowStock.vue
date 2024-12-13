<template>
  <div class="low-stock-container">
    <h2 class="low-stock-title">Produkty na wyczerpaniu</h2>
    <div v-if="products.length > 0" class="low-stock-grid">
      <div class="low-stock-card" v-for="product in products" :key="product.id">
        <h3 class="product-name">{{ product.name }}</h3>
        <p class="product-stock">Pozostało: <strong>{{ product.stock }}</strong> szt.</p>
      </div>
    </div>
    <div v-else>
      <p class="no-low-stock">Brak produktów na wyczerpaniu.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      products: [],
    };
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:5000/analysis/low-stock');
      this.products = response.data;
    } catch (error) {
      console.error(error);
    }
  },
};
</script>

<style scoped>
.low-stock-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.low-stock-title {
  font-size: 2rem;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.low-stock-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.low-stock-card {
  background-color: #ffffff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.low-stock-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.product-name {
  font-size: 1.2rem;
  color: #2196f3;
  margin-bottom: 10px;
}

.product-stock {
  font-size: 1rem;
  color: #333;
}

.no-low-stock {
  text-align: center;
  font-size: 1.2rem;
  color: #f44336;
}
</style>
