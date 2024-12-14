<template>
  <div>
    <div class="product-grid">
      <div
        v-for="product in paginatedProducts"
        :key="product.id"
        class="product-card"
      >
        <router-link :to="`/product/${product.id}`">
          <img :src="product.image_url" alt="Product Image" class="product-image" />
        </router-link>
        <router-link :to="`/product/${product.id}`" class="product-name-link">
          <h3 class="product-name">{{ product.name }}</h3>
        </router-link>
        <p class="product-price">Cena: {{ product.price }} zł</p>
        <p class="product-stock">W magazynie: {{ product.stock }}</p>
        <button class="add-to-cart-button" @click="addToCart(product.id)">Dodaj do koszyka</button>
      </div>
    </div>

    <button v-if="showMoreAvailable" class="show-more-button" @click="showMore">Pokaż więcej</button>

    <div v-if="showSnackbar" class="snackbar">{{ snackbarMessage }}</div>
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
      snackbarMessage: '',
      showSnackbar: false,
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
          ? `http://48.209.24.37:5000/category/${this.category}`
          : 'http://48.209.24.37:5000/products';
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
        this.showSnackbarMessage('Musisz być zalogowany, aby dodać produkty do koszyka!');
        return;
      }

      try {
        await axios.post(
          'http://48.209.24.37:5000/cart/add',
          { product_id: productId },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.showSnackbarMessage('Produkt dodany do koszyka!');
      } catch (error) {
        this.showSnackbarMessage('Wystąpił problem podczas dodawania do koszyka.');
      }
    },
    showSnackbarMessage(message) {
      this.snackbarMessage = message;
      this.showSnackbar = true;
      setTimeout(() => {
        this.showSnackbar = false;
      }, 3000);
    },
  },
  watch: {
    category: 'fetchProducts',
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>

<style scoped>
.page-title {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: #333;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.product-card {
  background-color: #ffffff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.3s, box-shadow 0.3s;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.product-image {
  max-width: 100%;
  height: auto;
  object-fit: contain;
  margin-bottom: 10px;
}

.product-name-link {
  text-decoration: none;
}

.product-name {
  color: #333;
  font-size: 1.2rem;
  margin: 10px 0;
}

.product-price,
.product-stock {
  font-size: 0.9rem;
  color: #666;
  margin: 5px 0;
}

.add-to-cart-button {
  background-color: #2196f3;
  color: #ffffff;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.add-to-cart-button:hover {
  background-color: #1e88e5;
}

.show-more-button {
  display: block;
  margin: 20px auto;
  background-color: #2196f3;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.show-more-button:hover {
  background-color: #1e88e5;
}

.snackbar {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  font-size: 1rem;
  animation: fadeInOut 3s ease-in-out;
}

@keyframes fadeInOut {
  0%, 100% {
    opacity: 0;
  }
  10%, 90% {
    opacity: 1;
  }
}
</style>
