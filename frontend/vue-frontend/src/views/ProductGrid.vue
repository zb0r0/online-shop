<template>
  <div>
    <h2 v-if="category">Produkty w kategorii: {{ category }}</h2>
    <h2 v-else>Produkty</h2>
    <div class="product-grid">
      <div
        v-for="product in paginatedProducts"
        :key="product.id"
        class="product-card"
      >
        <router-link :to="`/product/${product.id}`">
          <img :src="product.image_url" alt="Product Image" />
        </router-link>
        <router-link :to="`/product/${product.id}`">
          <h3>{{ product.name }}</h3>
        </router-link>
        <p>Cena: {{ product.price }} zł</p>
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
  props: {
    category: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      products: [],
      rowsToShow: 5,
      columnsPerRow: 5,
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
        const endpoint = this.category
          ? `http://localhost:5000/category/${this.category}`
          : 'http://localhost:5000/products';
        const response = await axios.get(endpoint);
        this.products = response.data;
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    },
    showMore() {
      this.rowsToShow += 5;
    },
    async addToCart(productId) {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Musisz być zalogowany, aby dodać produkty do koszyka!');
        return;
      }

      try {
        const response = await axios.post(
          'http://localhost:5000/cart/add',
          { product_id: productId },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        alert(response.data.message);
      } catch (error) {
        alert(error.response?.data?.message || 'Wystąpił błąd');
      }
    },
  },
  watch: {
    category: 'fetchProducts', // Odswież produkty po zmianie kategorii
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
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.product-card img {
  max-width: 100%;
  height: auto;
  flex-grow: 1; /* Obrazek zajmuje dostępną przestrzeń w pionie */
  cursor: pointer; /* Dodanie wskazówki kliknięcia */
}
.product-card h3 {
  cursor: pointer; /* Dodanie wskazówki kliknięcia */
}
</style>
