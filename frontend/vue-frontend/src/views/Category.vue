<template>
  <div>
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
