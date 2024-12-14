<template>
  <div v-if="product" class="product-details-container">
    <div class="product-image-wrapper">
      <img :src="product.image_url" alt="Product Image" class="product-image" />
    </div>
    <div class="product-info">
      <h2 class="product-title">{{ product.name }}</h2>
      <p class="product-description">{{ product.description }}</p>
      <p class="product-price">Cena: {{ product.price }}zł</p>
      <p class="product-stock">W magazynie: {{ product.stock }}</p>
      <p class="product-category">Kategoria: {{ product.category }}</p>
      <button class="add-to-cart-button" @click="addToCart">Dodaj do koszyka</button>
    </div>
  </div>
  <div v-else class="loading-container">
    <p class="loading-text">Ładowanie...</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ProductDetails",
  data() {
    return {
      product: null,
    };
  },
  methods: {
    async fetchProduct() {
      const productId = this.$route.params.id;
      try {
        const response = await axios.get(`http://48.209.24.37:5000/product/${productId}`);
        this.product = response.data;
      } catch (error) {
        console.error("Error fetching product details:", error);
      }
    },
    async addToCart() {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Musisz być zalogowany, aby dodać produkt do koszyka!");
        return;
      }

      try {
        const response = await axios.post(
          "http://48.209.24.37:5000/cart/add",
          { product_id: this.product.id },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        alert(response.data.message);
      } catch (error) {
        alert(error.response?.data?.message || "Wystąpił błąd");
      }
    },
  },
  mounted() {
    this.fetchProduct();
  },
};
</script>

<style scoped>
.product-details-container {
  display: flex;
  gap: 30px;
  padding: 40px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  align-items: flex-start;
  min-height: 80vh;
}

.product-image-wrapper {
  flex: 1;
  max-width: 25%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  height: 80vh; /* Zwiększenie wysokości na 80% strony */
}

.product-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.product-info {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 20px;
  justify-content: center;
}

.product-title {
  font-size: 2rem;
  color: #333;
  margin-bottom: 10px;
}

.product-description {
  font-size: 1.2rem;
  color: #666;
  line-height: 1.8;
  margin-bottom: 20px;
}

.product-price {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2196f3;
}

.product-stock,
.product-category {
  font-size: 1.2rem;
  color: #333;
}

.add-to-cart-button {
  background-color: #2196f3;
  color: #ffffff;
  border: none;
  padding: 15px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.2rem;
  transition: background-color 0.3s;
  align-self: flex-start;
}

.add-to-cart-button:hover {
  background-color: #1e88e5;
}

.loading-container {
  text-align: center;
  padding: 50px 0;
}

.loading-text {
  font-size: 1.5rem;
  color: #666;
}
</style>
