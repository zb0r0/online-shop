<template>
  <div>
    <h2 class="category-title">{{ category }}</h2>
    <ProductGrid :category="category" />
  </div>
</template>

<script>
import ProductGrid from './ProductGrid.vue';

export default {
  name: 'CategoryView',
  components: {
    ProductGrid,
  },
  computed: {
    category() {
      return this.$route.params.category;
    },
  },
};
</script>

<style scoped>
.category-title {
  font-size: 2rem;
  color: #2196f3;
  text-align: center;
  margin: 20px 0;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
}
</style>
