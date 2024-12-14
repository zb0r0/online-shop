<template>
  <div class="cart-container">
    <h2 class="cart-title">Twój koszyk</h2>
    <div v-if="cart.length > 0" class="cart-content">
      <div v-for="item in cart" :key="item.id" class="cart-item">
        <router-link :to="`/product/${item.product_id}`" class="item-image-wrapper">
          <img :src="item.image_url" alt="Product Image" class="item-image" />
        </router-link>
        <div class="item-info">
          <router-link :to="`/product/${item.product_id}`" class="item-name">
            <h3>{{ item.name }}</h3>
          </router-link>
          <p class="item-price">Cena: {{ item.price }} zł</p>
          <div class="item-quantity">
            <button class="quantity-button" @click="updateQuantity(item, -1)">-</button>
            <span class="quantity">{{ item.quantity }}</span>
            <button class="quantity-button" @click="updateQuantity(item, 1)">+</button>
          </div>
          <button class="remove-item-button" @click="removeFromCart(item)">Usuń</button>
        </div>
      </div>
      <div class="cart-summary">
        <h3 class="total-price"><span>Łączna cena:</span> <strong>{{ totalPrice }} zł</strong></h3>
        <button class="checkout-button" @click="checkout">Zamów</button>
      </div>
    </div>
    <div v-else class="empty-cart">
      <p class="empty-cart-message">Twój koszyk jest pusty.</p>
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
        const response = await axios.get('http://48.209.24.37:5000/cart', {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.cart = response.data.cart;
        this.totalPrice = response.data.total_price;
      } catch (error) {
        alert(error.response?.data?.message || 'Wystąpił błąd');
      }
    },

    async updateQuantity(item, change) {
      const newQuantity = item.quantity + change;
      if (newQuantity < 1) return;
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Musisz być zalogowany, aby zaktualizować ilość!');
        return;
      }

      try {
        await axios.put(
          'http://48.209.24.37:5000/cart/update_quantity',
          {
            product_id: item.product_id,
            quantity: newQuantity,
          },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        item.quantity = newQuantity;
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
          'http://48.209.24.37:5000/cart/remove',
          {
            headers: { Authorization: `Bearer ${token}` },
            data: { product_id: item.product_id },
          }
        );
        this.cart = this.cart.filter(cartItem => cartItem.id !== item.id);
      } catch (error) {
        alert(error.response?.data?.message || 'Wystąpił błąd');
      }
    },

    checkout() {
      this.$router.push({ name: 'OrderPage' });
    },
  },
  computed: {
    totalPrice() {
      return this.cart.reduce((total, item) => total + item.price * item.quantity, 0);
    },
  },
  mounted() {
    this.fetchCart();
  },
};
</script>

<style scoped>
.cart-container {
  padding: 40px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.cart-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 20px;
  color: #333;
}

.cart-content {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.cart-item {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.item-image-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.item-image {
  max-width: 80%;
  max-height: 150px;
  object-fit: contain;
  margin-bottom: 15px;
}

.item-info {
  text-align: center;
}

.item-name {
  text-decoration: none;
  color: #333;
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.item-price {
  font-size: 1rem;
  color: #2196f3;
  margin-bottom: 10px;
}

.item-quantity {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.quantity-button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.quantity-button:hover {
  background-color: #45a049;
}

.quantity {
  font-size: 1.2rem;
}

.remove-item-button {
  background-color: #f44336;
  color: #ffffff;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.remove-item-button:hover {
  background-color: #d32f2f;
}

.cart-summary {
  text-align: right;
  margin-top: 20px;
}

.total-price {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.checkout-button {
  background-color: #4caf50;
  color: #ffffff;
  border: none;
  padding: 15px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.2rem;
  transition: background-color 0.3s;
}

.checkout-button:hover {
  background-color: #45a049;
}

.empty-cart {
  text-align: center;
  padding: 50px 0;
}

.empty-cart-message {
  font-size: 1.5rem;
  color: #666;
}
</style>
