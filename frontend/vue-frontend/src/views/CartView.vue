<template>
  <div>
    <h2>Twój koszyk</h2>
    <div v-if="cart.length > 0">
      <div v-for="item in cart" :key="item.id" class="cart-item">
        <img :src="item.image_url" alt="Product Image" />
        <div>
          <h3>{{ item.name }}</h3>
          <p>Cena: {{ item.price }}zł</p>
          <p>Ilość:
            <input type="number" v-model="item.quantity" min="1" @blur="updateQuantity(item)">
          </p>
          <button @click="removeFromCart(item)">Usuń</button>
        </div>
      </div>
      <h3>Łączna cena: {{ totalPrice }}zł</h3>
      <button @click="checkout">Zamów</button>
    </div>
    <div v-else>
      <p>Twój koszyk jest pusty.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CartPage',
  data() {
    return {
      cart: [],
      totalPrice: 0,
    };
  },
  methods: {
    async fetchCart() {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('You must be logged in to view your cart!');
        return;
      }

      try {
        const response = await axios.get('http://localhost:5000/cart', {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.cart = response.data.cart;
        this.totalPrice = response.data.total_price;
      } catch (error) {
        alert(error.response?.data?.message || 'An error occurred');
      }
    },

    async updateQuantity(item) {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('You must be logged in to update the quantity!');
        return;
      }

      try {
        const response = await axios.put(
          'http://localhost:5000/cart/update_quantity',
          {
            product_id: item.product_id,
            quantity: item.quantity,
          },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        // Aktualizacja ceny po zmianie ilości
        this.totalPrice = response.data.total_price;
      } catch (error) {
        alert(error.response?.data?.message || 'An error occurred');
      }
    },

    async removeFromCart(item) {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('You must be logged in to remove products from your cart!');
        return;
      }

      try {
        await axios.delete(
          'http://localhost:5000/cart/remove',
          {
            headers: { Authorization: `Bearer ${token}` },
            data: { product_id: item.product_id },
          }
        );
        // Usuwanie produktu z koszyka
        this.cart = this.cart.filter(cartItem => cartItem.id !== item.id);
        // Aktualizacja łącznej ceny
        this.totalPrice = this.cart.reduce((total, item) => total + (item.price * item.quantity), 0);
      } catch (error) {
        alert(error.response?.data?.message || 'An error occurred');
      }
    },

    checkout() {
      this.$router.push({ name: 'OrderPage' });
    },
  },
  mounted() {
    this.fetchCart();
  },
};
</script>

<style scoped>
.cart-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.cart-item img {
  width: 100px;
  height: auto;
  margin-right: 20px;
}

input[type="number"] {
  width: 50px;
  margin-left: 10px;
}
</style>
