<template>
  <div>
    <main>
      <ProductGrid />
    </main>
  </div>
</template>

<script>
import ProductGrid from '@/views/ProductGrid.vue';

export default {
  name: 'HomePage',
  components: {
    ProductGrid,
  },
};
</script>

<style scoped>
main {
  width: 100%;
  display: flex;
  justify-content: center;
}
</style>
