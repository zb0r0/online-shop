<template>
  <div>
    <h2>Najaktywniejsi kupujący</h2>
    <div v-if="customers.length > 0">
      <ul>
        <li v-for="customer in customers" :key="customer.username">
          {{ customer.username }}: {{ formatCurrency(customer.total_spent) }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>Brak danych o kupujących.</p>
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
      const response = await axios.get('http://localhost:5000/analysis/top-customers');
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
