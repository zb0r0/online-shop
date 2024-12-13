<template>
  <div>
    <h2>Trendy sprzedażowe</h2>

    <!-- Wybór dat -->
    <div>
      <label for="start-date">Wybierz datę początkową:</label>
      <input type="date" v-model="startDate" @change="fetchTrends" />

      <label for="end-date">Wybierz datę końcową:</label>
      <input type="date" v-model="endDate" @change="fetchTrends" />
    </div>

    <!-- Przycisk wyboru ostatniego tygodnia, miesiąca, kwartału -->
    <div>
      <button @click="setDateRange('week')">Ostatni tydzień</button>
      <button @click="setDateRange('month')">Ostatni miesiąc</button>
      <button @click="setDateRange('quarter')">Ostatni kwartał</button>
    </div>

    <div v-if="trends.length > 0">
      <h3>Wyniki</h3>

      <!-- Wykres słupkowy -->
      <div class="chart-container">
        <canvas id="salesChart"></canvas>
      </div>
    </div>

    <div v-else>
      <p>Brak danych dla wybranego okresu.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController } from 'chart.js';

// Rejestracja kontrolera, elementów i skal w Chart.js
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController);

export default {
  data() {
    return {
      startDate: '',
      endDate: '',
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
      if (!this.startDate || !this.endDate) {
        return; // Zatrzymanie funkcji, jeśli daty nie zostały wybrane
      }

      try {
        let url = `http://localhost:5000/analysis/trends?start_date=${this.startDate}&end_date=${this.endDate}`;
        const response = await axios.get(url);

        // Sprawdzanie, czy dane zostały zwrócone
        if (response.data.length > 0) {
          this.trends = response.data;

          // Użyj $nextTick, aby poczekać na renderowanie DOM
          this.$nextTick(() => {
            this.renderChart();  // Rysowanie wykresu po załadowaniu danych
          });
        } else {
          this.trends = [];
        }
      } catch (error) {
        console.error(error);
        this.trends = [];
      }
    },

    // Ustawienie zakresu dat na podstawie przycisków
    setDateRange(range) {
      const today = new Date();
      let startDate;
      let endDate = today.toISOString().split('T')[0];  // dzisiejsza data (end date)

      switch (range) {
        case 'week':
          startDate = new Date(today);
          startDate.setDate(today.getDate() - 7);
          startDate = startDate.toISOString().split('T')[0];
          break;
        case 'month':
          startDate = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
          startDate = startDate.toISOString().split('T')[0];
          break;
        case 'quarter':
          startDate = new Date(today.getFullYear(), today.getMonth() - 3, today.getDate());
          startDate = startDate.toISOString().split('T')[0];
          break;
      }

      this.startDate = startDate;
      this.endDate = endDate;

      // Po ustawieniu dat, wykonaj fetch
      this.fetchTrends();
    },

    renderChart() {
      const canvas = document.getElementById('salesChart');

      // Sprawdzenie, czy istnieje wykres i jego usunięcie
      if (window.myChart) {
        window.myChart.destroy();  // Zniszczenie starego wykresu
      }

      const ctx = canvas.getContext('2d');
      if (ctx) {
        const labels = this.trends.map(trend => trend.product_name);
        const data = this.trends.map(trend => trend.total_quantity);

        // Tworzenie nowego wykresu
        window.myChart = new ChartJS(ctx, {
          type: 'bar', // Typ wykresu
          data: {
            labels: labels,
            datasets: [{
              label: 'Ilość sprzedanych produktów',
              data: data,
              backgroundColor: '#42A5F5',
              borderColor: '#1E88E5',
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            scales: {
              x: {
                beginAtZero: true
              },
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }
    },
  },
};
</script>

<style scoped>
.chart-container {
  width: 70%;
  height: 50vh;
  margin: 0 auto;
}
</style>
