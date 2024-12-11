<template>
  <div>
    <h2>Produkty na wyczerpaniu</h2>
    <div v-if="products.length > 0">
      <ul>
        <li v-for="product in products" :key="product.id">
          {{ product.name }}: {{ product.stock }} szt.
        </li>
      </ul>
    </div>
    <div v-else>
      <p>Brak produktów na wyczerpaniu.</p>
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
