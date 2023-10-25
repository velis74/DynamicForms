<template>
  <div>
    <label v-if="label">{{ label }}</label>
    <v-input
      :messages="messages"
      :error-messages="errorMessages"
      :error-count="errorCount"
    >
      <slot/>
    </v-input>
  </div>
</template>

<script setup lang="ts">

interface Props {
  //props
  label: string
  errorMessages: string[]
  errorCount: number
  messages: string[]
}

defineProps<Props>();


</script>


<style scoped>

</style>
