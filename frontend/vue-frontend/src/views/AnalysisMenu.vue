<template>
  <div class="analysis-menu">
    <nav>
      <ul>
        <li><router-link to="/analysis/trends">Trendy sprzedażowe</router-link></li>
        <li><router-link to="/analysis/top-customers">Najaktywniejsi kupujący</router-link></li>
        <li><router-link to="/analysis/low-stock">Produkty na wyczerpaniu</router-link></li>
        <li><router-link to="/analysis/earnings">Zarobki</router-link></li>
      </ul>
    </nav>
    <div class="analysis-content">
      <router-view />  <!-- Tutaj będą renderowane podstrony analityczne -->
    </div>
  </div>
</template>

<style scoped>
.analysis-menu {
  display: flex;
  height: 100vh;  /* Wysokość na cały ekran */
}

nav {
  width: 200px;
  border-right: 1px solid #ccc;
  padding-right: 10px;
  height: 100%;  /* Zapewnia, że menu zajmuje całą wysokość */
  background-color: #f9f9f9;  /* Opcjonalnie, zmienia tło na jaśniejsze */
}

nav ul {
  list-style: none;
  padding: 0;
}

nav li {
  margin-bottom: 10px;
}

.analysis-content {
  flex: 1;  /* Zapewnia, że przestrzeń dla zawartości będzie elastyczna */
  padding: 20px;  /* Dodaje margines dookoła zawartości */
  height: 100%;  /* Wysokość na cały ekran */
  overflow-y: auto;  /* Pozwala przewijać zawartość, jeśli jest za długa */
}
</style>
<script setup>
</script>