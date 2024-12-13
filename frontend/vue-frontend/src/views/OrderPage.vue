<template>
  <div class="checkout-container">
    <h2 class="checkout-title">Podaj dane do wysyłki</h2>
    <form @submit.prevent="submitOrder" class="checkout-form">
      <div class="form-group">
        <label for="first_name">Imię:</label>
        <input v-model="form.first_name" type="text" id="first_name" required />
      </div>

      <div class="form-group">
        <label for="last_name">Nazwisko:</label>
        <input v-model="form.last_name" type="text" id="last_name" required />
      </div>

      <div class="form-group">
        <label for="email">E-mail:</label>
        <input v-model="form.email" type="text" id="email" required />
      </div>

      <div class="form-group">
        <label for="address">Adres:</label>
        <input v-model="form.address" type="text" id="address" required />
      </div>

      <div class="form-group">
        <label for="zip_code">Kod pocztowy:</label>
        <input v-model="form.zip_code" type="text" id="zip_code" required />
      </div>

      <div class="form-group">
        <label for="city">Miasto:</label>
        <input v-model="form.city" type="text" id="city" required />
      </div>

      <div class="form-group">
        <label for="phone">Numer telefonu:</label>
        <input v-model="form.phone" type="text" id="phone" required />
      </div>

      <div class="form-group">
        <label for="total">Kwota do zapłaty:</label>
        <input :value="calculatedTotal" type="text" id="total" disabled />
      </div>

      <button type="submit" class="submit-button">Przejdź do płatności</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CheckoutView',
  data() {
    return {
      form: {
        first_name: '',
        last_name: '',
        email: '',
        address: '',
        zip_code: '',
        city: '',
        phone: '',
        total: 0,
      },
      cart: [],
    };
  },
  computed: {
    calculatedTotal() {
      let total = 0;
      this.cart.forEach(item => {
        total += item.price * item.quantity;
      });
      return total.toFixed(2);
    },
  },
  mounted() {
    this.loadCart();
  },
  methods: {
    async loadCart() {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Musisz być zalogowany, aby zobaczyć koszyk!');
        return;
      }

      try {
        const response = await axios.get('http://localhost:5000/cart', {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.cart = response.data.cart;
        this.form.total = response.data.total_price;
      } catch (error) {
        alert(error.response?.data?.message || 'Błąd podczas ładowania koszyka');
      }
    },

    async submitOrder() {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Musisz być zalogowany, aby złożyć zamówienie!');
        return;
      }

      try {
        const orderData = { ...this.form, total: this.calculatedTotal };
        const response = await axios.post(
          'http://localhost:5000/orders',
          orderData,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        this.$router.push({
          name: 'OrderSuccess',
          params: { id: response.data.order_id },
        });
      } catch (error) {
        alert(error.response?.data?.message || 'Wystąpił błąd');
      }
    },
  },
};
</script>

<style scoped>
.checkout-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.checkout-title {
  font-size: 2rem;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.checkout-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-size: 1rem;
  color: #333;
  margin-bottom: 5px;
}

input {
  font-size: 1rem;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  outline: none;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #2196f3;
}

.submit-button {
  background-color: #4caf50;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #45a049;
}
</style>
