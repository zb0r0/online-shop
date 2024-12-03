<template>
  <div>
    <p>Przekierowanie na stronę główną...</p>
  </div>
</template>

<script>
export default {
  name: "RedirectToHome",
  mounted() {
    this.$router.push("/");
  },
};
</script>

<style scoped>
p {
  text-align: center;
  margin-top: 20px;
  font-size: 18px;
  color: #555;
}
</style>
