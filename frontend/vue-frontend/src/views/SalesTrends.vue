<template>
  <div class="trends-container">
    <h2 class="trends-title">Trendy sprzedażowe</h2>

    <div class="date-selection">
      <div class="date-group">
        <label for="start-date" class="date-label">Wybierz datę początkową:</label>
        <input type="date" v-model="startDate" @change="fetchTrends" class="date-input" />
      </div>

      <div class="date-group">
        <label for="end-date" class="date-label">Wybierz datę końcową:</label>
        <input type="date" v-model="endDate" @change="fetchTrends" class="date-input" />
      </div>
    </div>

    <div class="range-buttons">
      <button @click="setDateRange('week')" class="range-button">Ostatni tydzień</button>
      <button @click="setDateRange('month')" class="range-button">Ostatni miesiąc</button>
      <button @click="setDateRange('quarter')" class="range-button">Ostatni kwartał</button>
    </div>

    <div v-if="trends.length > 0">
      <h3 class="results-title">Wyniki</h3>
      <div class="chart-container">
        <canvas id="salesChart"></canvas>
      </div>
    </div>

    <div v-else>
      <p class="no-data">Brak danych dla wybranego okresu.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController);

export default {
  data() {
    return {
      startDate: '',
      endDate: '',
      trends: [],
    };
  },
  methods: {
    async fetchTrends() {
      if (!this.startDate || !this.endDate) {
        return;
      }

      try {
        const response = await axios.get(`http://localhost:5000/analysis/trends?start_date=${this.startDate}&end_date=${this.endDate}`);
        if (response.data.length > 0) {
          this.trends = response.data;
          this.$nextTick(() => {
            this.renderChart();
          });
        } else {
          this.trends = [];
        }
      } catch (error) {
        console.error(error);
        this.trends = [];
      }
    },

    setDateRange(range) {
      const today = new Date();
      let startDate;
      const endDate = today.toISOString().split('T')[0];

      switch (range) {
        case 'week':
          startDate = new Date(today);
          startDate.setDate(today.getDate() - 7);
          break;
        case 'month':
          startDate = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
          break;
        case 'quarter':
          startDate = new Date(today.getFullYear(), today.getMonth() - 3, today.getDate());
          break;
      }

      this.startDate = startDate.toISOString().split('T')[0];
      this.endDate = endDate;
      this.fetchTrends();
    },

    renderChart() {
      const canvas = document.getElementById('salesChart');
      if (window.myChart) {
        window.myChart.destroy();
      }

      const ctx = canvas.getContext('2d');
      if (ctx) {
        const labels = this.trends.map(trend => trend.product_name);
        const data = this.trends.map(trend => trend.total_quantity);

        window.myChart = new ChartJS(ctx, {
          type: 'bar',
          data: {
            labels,
            datasets: [{
              label: 'Ilość sprzedanych produktów',
              data,
              backgroundColor: '#42A5F5',
              borderColor: '#1E88E5',
              borderWidth: 1,
            }],
          },
          options: {
            responsive: true,
            scales: {
              x: { beginAtZero: true },
              y: { beginAtZero: true },
            },
          },
        });
      }
    },
  },
};
</script>

<style scoped>
.trends-container {
  max-width: 1000px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.trends-title {
  font-size: 2rem;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.date-selection {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.date-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-label {
  font-size: 1rem;
  color: #333;
}

.date-input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.range-buttons {
  text-align: center;
  margin-bottom: 30px;
}

.range-button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 15px;
  margin: 0 5px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.range-button:hover {
  background-color: #45a049;
}

.results-title {
  font-size: 1.5rem;
  color: #2196f3;
  margin-bottom: 15px;
}

.chart-container {
  width: 100%;
  height: 50vh;
  margin: 0 auto;
}

.no-data {
  text-align: center;
  font-size: 1.2rem;
  color: #f44336;
}
</style>