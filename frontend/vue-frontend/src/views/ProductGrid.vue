<template>
  <div>
    <h2>Produkty</h2>
    <div class="product-grid">
      <div
        v-for="product in paginatedProducts"
        :key="product.id"
        class="product-card"
      >
        <img :src="product.image_url" alt="Product Image" />
        <h3>{{ product.name }}</h3>
        <p>Cena: {{ product.price }}zł</p>
        <p>W magazynie: {{ product.stock }}</p>
        <button @click="addToCart(product.id)">Dodaj do koszyka</button>
      </div>
    </div>

    <button v-if="showMoreAvailable" @click="showMore">Pokaż więcej</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProductGrid',
  data() {
    return {
      products: [],
      rowsToShow: 5, // liczba wierszy do wyświetlenia na raz
      columnsPerRow: 5, // liczba kolumn na wiersz
    };
  },
  computed: {
    paginatedProducts() {
      const itemsPerPage = this.rowsToShow * this.columnsPerRow;
      return this.products.slice(0, itemsPerPage);
    },
    showMoreAvailable() {
      return this.paginatedProducts.length < this.products.length;
    },
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('http://localhost:5000/products');
        this.products = response.data;
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    },
    showMore() {
      this.rowsToShow += 5; // zwiększamy liczbę widocznych wierszy
    },
    addToCart(productId) {
      // Dodaj logikę dodawania do koszyka
      console.log(`Added product ${productId} to cart`);
    },
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>

<style scoped>
.product-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr); /* 5 kolumn */
  gap: 20px;
}
.product-card {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}
.product-card img {
  max-width: 100%;
  height: auto;
}
</style>
