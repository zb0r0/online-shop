<template>
  <div>
    <h2>Trendy sprzedażowe</h2>
    <label for="month">Wybierz miesiąc:</label>
    <select v-model="selectedMonth" @change="fetchTrends">
      <option v-for="month in months" :key="month.value" :value="month.value">{{ month.label }}</option>
    </select>
    <div v-if="trends.length > 0">
      <h3>Wyniki</h3>
      <ul>
        <li v-for="trend in trends" :key="trend.product_name">
          {{ trend.product_name }}: {{ trend.total_quantity }} szt.
        </li>
      </ul>
    </div>
    <div v-else>
      <p>Brak danych dla wybranego miesiąca.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedMonth: 1,
      trends: [],
      months: [
        { value: 1, label: "Styczeń" },
        { value: 2, label: "Luty" },
        { value: 3, label: "Marzec" },
        { value: 4, label: "Kwiecień" },
        { value: 5, label: "Maj" },
        { value: 6, label: "Czerwiec" },
        { value: 7, label: "Lipiec" },
        { value: 8, label: "Sierpień" },
        { value: 9, label: "Wrzesień" },
        { value: 10, label: "Październik" },
        { value: 11, label: "Listopad" },
        { value: 12, label: "Grudzień" },
      ],
    };
  },
  methods: {
    async fetchTrends() {
      try {
        const response = await axios.get(`http://localhost:5000/analysis/trends?month=${this.selectedMonth}`);
        this.trends = response.data;
      } catch (error) {
        console.error(error);
        this.trends = [];
      }
    },
  },
};
</script>
