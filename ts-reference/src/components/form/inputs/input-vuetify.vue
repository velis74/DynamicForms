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

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'VuetifyInput',
  props: {
    label: { default: null, type: String },
    errorMessages: { default: () => [], type: Array },
    errorCount: { default: 0, type: Number },
    messages: { default: () => [], type: Array },
  },
});
</script>
