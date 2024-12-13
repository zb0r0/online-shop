<template>
  <div class="earnings-container">
    <h2 class="earnings-title">Analiza zarobków</h2>

    <div class="view-selection">
      <div class="view-group">
        <label for="view-type" class="view-label">Wybierz typ widoku:</label>
        <select v-model="viewType" @change="fetchEarnings" class="view-input">
          <option value="year">Roczny</option>
          <option value="month">Miesięczny</option>
          <option value="day">Dzienny</option>
        </select>
      </div>

      <div class="view-group" v-if="viewType !== 'year'">
        <label class="view-label">Rok:</label>
        <input
          type="number"
          v-model="year"
          min="2000"
          :max="new Date().getFullYear()"
          placeholder="Rok"
          @change="fetchEarnings"
          class="view-input"
        />
      </div>

      <div class="view-group" v-if="viewType === 'day'">
        <label class="view-label">Miesiąc:</label>
        <select v-model="month" @change="fetchEarnings" class="view-input">
          <option v-for="m in months" :key="m.value" :value="m.value">{{ m.label }}</option>
        </select>
      </div>
    </div>

    <div v-if="earnings.length > 0">
      <h3 class="results-title">Wyniki</h3>
      <div class="chart-container">
        <canvas id="earningsChart"></canvas>
      </div>
    </div>

    <div v-else>
      <p class="no-data">Brak danych dla wybranego okresu.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  BarController,
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController);

export default {
  data() {
    return {
      viewType: 'year',
      year: new Date().getFullYear(),
      month: 1,
      earnings: [],
      months: [
        { value: 1, label: 'Styczeń' },
        { value: 2, label: 'Luty' },
        { value: 3, label: 'Marzec' },
        { value: 4, label: 'Kwiecień' },
        { value: 5, label: 'Maj' },
        { value: 6, label: 'Czerwiec' },
        { value: 7, label: 'Lipiec' },
        { value: 8, label: 'Sierpień' },
        { value: 9, label: 'Wrzesień' },
        { value: 10, label: 'Październik' },
        { value: 11, label: 'Listopad' },
        { value: 12, label: 'Grudzień' },
      ],
    };
  },
  methods: {
    async fetchEarnings() {
      const params = {
        view_type: this.viewType,
        year: this.year,
        month: this.viewType === 'day' ? this.month : undefined,
      };

      try {
        const response = await axios.get('http://localhost:5000/analysis/earnings', { params });
        this.earnings = this.processEarnings(response.data || []);
        this.$nextTick(() => this.renderChart());
      } catch (error) {
        console.error('Error fetching earnings:', error);
        this.earnings = [];
      }
    },

    processEarnings(rawEarnings) {
      if (this.viewType === 'day') {
        const daysInMonth = new Date(this.year, this.month, 0).getDate();
        const earningsMap = new Map(rawEarnings.map(e => [e.day, e.total_earnings]));

        return Array.from({ length: daysInMonth }, (_, i) => ({
          day: i + 1,
          total_earnings: earningsMap.get(i + 1) || 0,
        }));
      } else if (this.viewType === 'month') {
        const earningsMap = new Map(rawEarnings.map(e => [e.month, e.total_earnings]));

        return this.months.map(m => ({
          month: m.value,
          total_earnings: earningsMap.get(m.value) || 0,
        }));
      } else if (this.viewType === 'year') {
        return rawEarnings.map(e => ({
          year: e.year,
          total_earnings: e.total_earnings,
        }));
      }
      return rawEarnings;
    },

    renderChart() {
      if (!this.earnings.length) return;

      const canvas = document.getElementById('earningsChart');

      if (window.myEarningsChart) {
        window.myEarningsChart.destroy();
      }

      const ctx = canvas.getContext('2d');
      if (ctx) {
        const labels = this.earnings.map(e => {
          if (this.viewType === 'year') return e.year;
          if (this.viewType === 'month') return this.months[e.month - 1]?.label;
          return `Dzień ${e.day}`;
        });
        const data = this.earnings.map(e => e.total_earnings);

        window.myEarningsChart = new ChartJS(ctx, {
          type: 'bar',
          data: {
            labels,
            datasets: [
              {
                label: 'Zarobki (PLN)',
                data,
                backgroundColor: '#36A2EB',
                borderColor: '#36A2EB',
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                display: true,
                position: 'top',
              },
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: this.viewType === 'year' ? 'Rok' : this.viewType === 'month' ? 'Miesiąc' : 'Dzień',
                },
                beginAtZero: true,
              },
              y: {
                title: {
                  display: true,
                  text: 'Zarobki (PLN)',
                },
                beginAtZero: true,
              },
            },
          },
        });
      }
    },
  },
  mounted() {
    this.fetchEarnings();
  },
};
</script>

<style scoped>
.earnings-container {
  max-width: 1000px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.earnings-title {
  font-size: 2rem;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.view-selection {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  margin-bottom: 20px;
}

.view-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.view-label {
  font-size: 1rem;
  color: #333;
}

.view-input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.chart-container {
  width: 100%;
  height: 50vh;
  margin: 0 auto;
}

.results-title {
  font-size: 1.5rem;
  color: #2196f3;
  margin-bottom: 15px;
}

.no-data {
  text-align: center;
  font-size: 1.2rem;
  color: #f44336;
}
</style>
