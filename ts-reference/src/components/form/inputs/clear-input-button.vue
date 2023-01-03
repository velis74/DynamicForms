<template>
  <div class="field-clear-icon" @click="clear">
    <IonIcon name="trash-outline"/>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import IonIcon from 'vue-ionicon';

export default defineComponent({
  name: 'DInputClearButton',
  components: { IonIcon },
  methods: {
    clear() {
      this.$emit('clearButtonPressed');
    },
  },
});
</script>
