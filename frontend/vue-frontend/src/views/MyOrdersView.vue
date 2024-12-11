<template>
  <div>
    <h2>Twoje zamówienia</h2>
    <p>Poniżej znajdziesz listę swoich zamówień:</p>

    <div v-if="orders.length > 0" class="orders-grid">
      <div
        class="order-card"
        v-for="order in orders"
        :key="order.order_id"
        @click="goToOrderDetails(order.order_id)"
      >
        <h3>Zamówienie #{{ order.order_id }}</h3>
        <p><strong>Data:</strong> {{ order.created_at }}</p>
        <p><strong>Kwota:</strong> {{ order.total }} PLN</p>
        <p><strong>Status:</strong> {{ order.status }}</p>
      </div>
    </div>
    <div v-else>
      <p>Nie masz jeszcze żadnych zamówień.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MyOrdersView",
  data() {
    return {
      orders: [], // Lista zamówień użytkownika
    };
  },
  mounted() {
    this.loadOrders();
  },
  methods: {
    async loadOrders() {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Musisz być zalogowany, aby zobaczyć swoje zamówienia.");
        return;
      }

      try {
        const response = await axios.get("http://localhost:5000/user/orders", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.orders = response.data;
      } catch (error) {
        alert(
          error.response?.data?.message ||
            "Wystąpił błąd podczas ładowania zamówień."
        );
      }
    },
    goToOrderDetails(orderId) {
      this.$router.push(`/order-success/${orderId}`);
    },
  },
};
</script>

<style scoped>
.orders-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
  margin-top: 1rem;
}

.order-card {
  border: 1px solid #ddd;
  padding: 16px;
  border-radius: 8px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: transform 0.2s;
}

.order-card:hover {
  transform: scale(1.02);
}

.order-card h3 {
  margin: 0 0 8px;
  font-size: 1.2rem;
}

.order-card p {
  margin: 4px 0;
}
</style>
