<template>
  <div class="order-success-container">
    <h2 class="order-success-title">Twoje zamówienie zostało złożone pomyślnie!</h2>
    <p class="order-success-message">Dziękujemy za zakupy! Poniżej znajdziesz szczegóły swojego zamówienia:</p>

    <div v-if="order" class="order-details">
      <h3 class="order-section-title">Podsumowanie zamówienia</h3>
      <ul class="order-summary">
        <li><strong>Numer zamówienia:</strong> {{ order.order_id || 'Brak danych' }}</li>
        <li><strong>Data zamówienia:</strong> {{ order.created_at || 'Brak danych' }}</li>
        <li><strong>Kwota:</strong> {{ order.total ? `${order.total} PLN` : 'Brak danych' }}</li>
      </ul>

      <h3 class="order-section-title">Produkty</h3>
      <table class="order-table" v-if="order.products && order.products.length > 0">
        <thead>
          <tr>
            <th>Nazwa produktu</th>
            <th>Ilość</th>
            <th>Cena jednostkowa</th>
            <th>Łączna cena</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in order.products" :key="item.product_id">
            <td>{{ item.name || 'Brak danych' }}</td>
            <td>{{ item.quantity || 0 }}</td>
            <td>{{ item.price ? `${item.price} PLN` : 'Brak danych' }}</td>
            <td>{{ item.price && item.quantity ? `${(item.price * item.quantity).toFixed(2)} PLN` : 'Brak danych' }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="no-products">Brak produktów w zamówieniu.</p>

      <h3 class="order-section-title">Dane do wysyłki</h3>
      <ul class="shipping-details">
        <li><strong>Imię i nazwisko:</strong> {{ order.first_name || 'Brak danych' }} {{ order.last_name || 'Brak danych' }}</li>
        <li><strong>Adres:</strong> {{ order.address || 'Brak danych' }}, {{ order.zip_code || 'Brak danych' }} {{ order.city || 'Brak danych' }}</li>
        <li><strong>Telefon:</strong> {{ order.phone || 'Brak danych' }}</li>
      </ul>
    </div>
    <div v-else class="loading-message">
      <p>Ładowanie szczegółów zamówienia...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "OrderSuccessView",
  data() {
    return {
      order: null,
    };
  },
  mounted() {
    this.loadOrderDetails();
  },
  methods: {
    async loadOrderDetails() {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Musisz być zalogowany, aby zobaczyć swoje zamówienie.");
        return;
      }

      try {
        const orderId = this.$route.params.id;
        const response = await axios.get(
          `http://48.209.24.37:5000/orders/${orderId}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.order = response.data;
      } catch (error) {
        alert(
          error.response?.data?.message ||
            "Wystąpił błąd podczas ładowania szczegółów zamówienia."
        );
      }
    },
  },
};
</script>

<style scoped>
.order-success-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.order-success-title {
  font-size: 2rem;
  color: #4caf50;
  text-align: center;
  margin-bottom: 20px;
}

.order-success-message {
  text-align: center;
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 30px;
}

.order-section-title {
  font-size: 1.5rem;
  color: #2196f3;
  margin-top: 20px;
  margin-bottom: 10px;
}

.order-summary,
.shipping-details {
  list-style: none;
  padding: 0;
  margin: 0;
}

.order-summary li,
.shipping-details li {
  margin-bottom: 10px;
  font-size: 1rem;
  color: #333;
}

.order-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

.order-table th,
.order-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

.order-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

.no-products {
  font-size: 1rem;
  color: #f44336;
  margin-top: 10px;
}

.loading-message {
  text-align: center;
  font-size: 1.2rem;
  color: #666;
}
</style>