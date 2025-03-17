<template xmlns:v-slot="http://www.w3.org/1999/xhtml">
  <div>
    <label v-if="label">{{ label }}</label>
    <v-input
      :error-messages="errorMessages"
      :error-count="errorCount"
      :hint="hint"
      :persistent-hint="persistentHint"
      :hide-details="hideDetails"
    >
      <slot/>
    </v-input>
  </div>
</template>

<script setup lang="ts">
interface Props {
  // props
  label: string
  errorMessages: string[]
  errorCount: number
  hint?: string,
  persistentHint?: boolean,
  hideDetails?: boolean | 'auto',
}

defineProps<Props>();
</script>

<style scoped>

</style>
