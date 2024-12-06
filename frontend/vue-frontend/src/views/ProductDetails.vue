<template>
  <div v-if="product">
    <img :src="product.image_url" alt="Product Image" />
    <h2>{{ product.name }}</h2>
    <p>{{ product.description }}</p>
    <p>Cena: {{ product.price }}zł</p>
    <p>W magazynie: {{ product.stock }}</p>
    <p>Kategoria: {{ product.category }}</p>
    <button @click="addToCart">Dodaj do koszyka</button>
  </div>
  <div v-else>
    <p>Ładowanie...</p>
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
        const response = await axios.get(`https://48.209.24.37:5000/product/${productId}`);
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
          "https://48.209.24.37:5000/cart/add",
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
img {
  max-width: 100%;
  height: auto;
}
</style>
