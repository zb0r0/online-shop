<template>
  <div class="analysis-menu">
    <nav>
      <ul>
        <li><router-link to="/analysis/trends">Trendy sprzedażowe</router-link></li>
        <li><router-link to="/analysis/top-customers">Najaktywniejsi kupujący</router-link></li>
        <li><router-link to="/analysis/low-stock">Produkty na wyczerpaniu</router-link></li>
      </ul>
    </nav>
    <router-view />
  </div>
</template>

<style scoped>
.analysis-menu {
  display: flex;
}

nav {
  width: 200px;
  border-right: 1px solid #ccc;
  padding-right: 10px;
}

nav ul {
  list-style: none;
  padding: 0;
}

nav li {
  margin-bottom: 10px;
}
</style>
