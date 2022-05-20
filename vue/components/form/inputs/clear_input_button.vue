<template>
  <button
    type="button"
    :style="buttonStyle"
    @click="clear"
  >
    <IonIcon class="field-clear-icon" :style="iconStyle" name="trash-outline"/>
  </button>
</template>

<script>
import IonIcon from 'vue-ionicon';

export default {
  name: 'DInputClearButton',
  components: { IonIcon },
  props: {
    iconStyle: {
      type: String,
      default: 'float: right; transform: none;',
    },
    buttonStyle: {
      type: String,
      default: '',
    },
  },
  methods: {
    clear() {
      this.$emit('clearButtonPressed');
    },
  },
};
</script>

<style scoped>
.field-clear-icon {
  width: 1em;
  top: 55%;
  position: absolute;
  margin: 0;
  -ms-transform: translateY(-50%);
  transform: translateY(-50%);
}
</style>
