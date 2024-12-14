<template>
  <div class="customers-container">
    <h2 class="customers-title">Najaktywniejsi kupujący</h2>
    <div v-if="customers.length > 0" class="customers-list">
      <div class="customer-card" v-for="customer in customers" :key="customer.username">
        <h3 class="customer-name">{{ customer.username }}</h3>
        <p class="customer-spent">Wydane: <strong>{{ formatCurrency(customer.total_spent) }}</strong></p>
      </div>
    </div>
    <div v-else>
      <p class="no-customers">Brak danych o kupujących.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      customers: [],
    };
  },
  async created() {
    try {
      const response = await axios.get('http://48.209.24.37:5000/analysis/top-customers');
      this.customers = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    formatCurrency(value) {
      return `${value.toFixed(2)} PLN`;
    },
  },
};
</script>

<style scoped>
.customers-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.customers-title {
  font-size: 2rem;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.customers-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.customer-card {
  background-color: #ffffff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.customer-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.customer-name {
  font-size: 1.2rem;
  color: #2196f3;
  margin-bottom: 10px;
}

.customer-spent {
  font-size: 1rem;
  color: #333;
}

.no-customers {
  text-align: center;
  font-size: 1.2rem;
  color: #f44336;
}
</style>
