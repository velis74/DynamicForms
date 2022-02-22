<template>
  <div>
    Custom Component Template Demo
    <div v-for="item in data">
      {{ item }}
    </div>
  </div>
</template>

<script>
export default {
  name: "CustomComponent",
  props: ["data"],
}
</script>

<style scoped>

</style>