<template>
  <div>
    <h2>Podaj dane do wysyłki</h2>
    <form @submit.prevent="submitOrder">
      <div class="form-group">
        <label for="first_name">Imię:</label>
        <input v-model="form.first_name" type="text" id="first_name" required />
      </div>

      <div class="form-group">
        <label for="last_name">Nazwisko:</label>
        <input v-model="form.last_name" type="text" id="last_name" required />
      </div>

      <div class="form-group">
        <label for="last_name">E-mail:</label>
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

      <!-- Kwota do zapłaty jest obliczana automatycznie -->
      <div class="form-group">
        <label for="total">Kwota do zapłaty:</label>
        <input :value="calculatedTotal" type="number" id="total" disabled />
      </div>

      <button type="submit">Przejdź do płatności</button>
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
      cart: [],  // Produkty w koszyku
    };
  },
  computed: {
    // Oblicza kwotę do zapłaty na podstawie produktów w koszyku
    calculatedTotal() {
      let total = 0;
      this.cart.forEach(item => {
        total += item.price * item.quantity; // Załóżmy, że item.price i item.quantity są dostępne
      });
      return total.toFixed(2); // Zwracamy wartość w formacie z dwoma miejscami po przecinku
    }
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
          headers: { Authorization: `Bearer ${token}` }
        });
        this.cart = response.data.cart;
        this.form.total = response.data.total_price;  // Pobieramy łączną kwotę z backendu
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
        const orderData = { ...this.form, total: this.calculatedTotal }; // Dodajemy obliczoną kwotę
        const response = await axios.post(
          'http://localhost:5000/orders', // Zmiana na właściwą trasę
          orderData,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        this.$router.push({
          name: 'OrderSuccess',
          params: { id: response.data.order_id }
        });
      } catch (error) {
        alert(error.response?.data?.message || 'Wystąpił błąd');
      }
    },
  },
};
</script>

<style scoped>
/* Dodajemy style, aby formularz był czytelny */
.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.5rem;
  box-sizing: border-box;
}

button {
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  width: 100%;
}

button:hover {
  background-color: #0056b3;
}
</style>
