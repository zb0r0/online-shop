<template>
  <div>
    <h2>Twoje zamówienie zostało złożone pomyślnie!</h2>
    <p>Dziękujemy za zakupy! Poniżej znajdziesz szczegóły swojego zamówienia:</p>

    <!-- Szczegóły zamówienia -->
    <div v-if="order">
      <h3>Podsumowanie zamówienia</h3>
      <ul>
        <li><strong>Numer zamówienia:</strong> {{ order.order_id || 'Brak danych' }}</li>
        <li><strong>Data zamówienia:</strong> {{ order.created_at || 'Brak danych' }}</li>
        <li><strong>Kwota:</strong> {{ order.total ? `${order.total} PLN` : 'Brak danych' }}</li>
      </ul>

      <h3>Produkty</h3>
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
      <p v-else>Brak produktów w zamówieniu.</p>

      <h3>Dane do wysyłki</h3>
      <ul>
        <li>
          <strong>Imię i nazwisko:</strong>
          {{ order.first_name || 'Brak danych' }} {{ order.last_name || 'Brak danych' }}
        </li>
        <li>
          <strong>Adres:</strong>
          {{ order.address || 'Brak danych' }},
          {{ order.zip_code || 'Brak danych' }}
          {{ order.city || 'Brak danych' }}
        </li>
        <li><strong>Telefon:</strong> {{ order.phone || 'Brak danych' }}</li>
      </ul>
    </div>
    <div v-else>
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
      order: null, // Szczegóły zamówienia
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
        // Pobierz szczegóły zamówienia na podstawie ID
        const orderId = this.$route.params.id; // ID zamówienia przekazywane w URL
        const response = await axios.get(
          `http://localhost:5000/orders/${orderId}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        // Przypisz dane z backendu do obiektu order
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
.order-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.order-table th,
.order-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.order-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

h3 {
  margin-top: 1.5rem;
}
</style>
