<template>
  <div class="field-clear-icon" @click="clear">
    <IonIcon name="trash-outline"/>
  </div>
</template>

<script>
import IonIcon from 'vue-ionicon';

export default {
  name: 'DInputClearButton',
  components: { IonIcon },
  methods: {
    clear() {
      this.$emit('clearButtonPressed');
    },
  },
};
</script>
