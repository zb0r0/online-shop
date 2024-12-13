<template>
  <div class="analysis-container">
    <nav class="analysis-menu">
      <ul class="menu-list">
        <li>
          <router-link to="/analysis/trends" class="menu-link">
            <i class="icon icon-trends"></i> Trendy sprzedażowe
          </router-link>
        </li>
        <li>
          <router-link to="/analysis/top-customers" class="menu-link">
            <i class="icon icon-customers"></i> Najaktywniejsi kupujący
          </router-link>
        </li>
        <li>
          <router-link to="/analysis/low-stock" class="menu-link">
            <i class="icon icon-low-stock"></i> Produkty na wyczerpaniu
          </router-link>
        </li>
        <li>
          <router-link to="/analysis/earnings" class="menu-link">
            <i class="icon icon-earnings"></i> Zarobki
          </router-link>
        </li>
      </ul>
    </nav>
    <div class="analysis-content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.analysis-container {
  display: flex;
  height: 100vh;
  background-color: #f9f9f9;
}

.analysis-menu {
  width: 250px;
  background-color: #3a3f47;
  color: #ffffff;
  padding: 20px;
  border-right: 1px solid #ddd;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.menu-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.menu-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #61dafb;
  font-size: 1.2rem;
  padding: 10px;
  border-radius: 5px;
  transition: background-color 0.3s, color 0.3s;
}

.menu-link .icon {
  margin-right: 10px;
  font-size: 1.5rem;
  color: #ffffff;
}

.menu-link:hover {
  background-color: #1e88e5;
  color: #ffffff;
}

.analysis-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #ffffff;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.05);
}
</style>