<template>
  <div>
    <h2>Twój koszyk</h2>
    <div v-if="cart.length > 0">
      <div v-for="item in cart" :key="item.id" class="cart-item">
        <router-link :to="`/product/${item.product_id}`">
          <img :src="item.image_url" alt="Product Image" />
        </router-link>
        <div>
          <router-link :to="`/product/${item.product_id}`">
            <h3>{{ item.name }}</h3>
          </router-link>
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
        alert('Musisz być zalogowany, aby zobaczyć swój koszyk!');
        return;
      }

      try {
        const response = await axios.get('http://localhost:5000/cart', {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.cart = response.data.cart;
        this.totalPrice = response.data.total_price;
      } catch (error) {
        alert(error.response?.data?.message || 'Wystąpił błąd');
      }
    },

    async updateQuantity(item) {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Musisz być zalogowany, aby zaktualizować ilość!');
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
        this.totalPrice = response.data.total_price;
      } catch (error) {
        alert(error.response?.data?.message || 'Wystąpił błąd');
      }
    },

    async removeFromCart(item) {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Musisz być zalogowany, aby usunąć produkty z koszyka!');
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
        this.cart = this.cart.filter(cartItem => cartItem.id !== item.id);
        this.totalPrice = this.cart.reduce((total, item) => total + (item.price * item.quantity), 0);
      } catch (error) {
        alert(error.response?.data?.message || 'Wystąpił błąd');
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
  cursor: pointer; /* Dodanie wskazówki kliknięcia */
}

.cart-item h3 {
  cursor: pointer; /* Dodanie wskazówki kliknięcia */
}

input[type="number"] {
  width: 50px;
  margin-left: 10px;
}
</style>
