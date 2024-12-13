<template>
  <div class="orders-container">
    <h2 class="orders-title">Twoje zamówienia</h2>
    <p class="orders-message">Poniżej znajdziesz listę swoich zamówień:</p>

    <div v-if="orders.length > 0" class="orders-grid">
      <div
        class="order-card"
        v-for="order in orders"
        :key="order.order_id"
        @click="goToOrderDetails(order.order_id)"
      >
        <h3 class="order-id">Zamówienie #{{ order.order_id }}</h3>
        <p><strong>Data:</strong> {{ order.created_at }}</p>
        <p><strong>Kwota:</strong> {{ order.total }} PLN</p>
        <p><strong>Status:</strong> {{ order.status }}</p>
      </div>
    </div>
    <div v-else>
      <p class="no-orders">Nie masz jeszcze żadnych zamówień.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MyOrdersView",
  data() {
    return {
      orders: [],
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
.orders-container {
  max-width: 1000px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.orders-title {
  font-size: 2rem;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.orders-message {
  text-align: center;
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 30px;
}

.orders-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.order-card {
  background-color: #ffffff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.order-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.order-id {
  font-size: 1.5rem;
  color: #2196f3;
  margin-bottom: 10px;
}

.order-card p {
  margin: 5px 0;
  font-size: 1rem;
  color: #333;
}

.no-orders {
  text-align: center;
  font-size: 1.2rem;
  color: #f44336;
}
</style>