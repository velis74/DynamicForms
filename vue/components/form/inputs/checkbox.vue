<template>
  <v-checkbox
    :id="field.uuid"
    v-model="value"
    indeterminate="indeterminate"
    :false-value="false"
    :true-value="true"
    :class="field.renderParams.fieldCSSClass"
    :name="field.name"
    :readonly="field.readOnly"
    :disabled="field.readOnly"

    v-bind="baseBinds"

    @change="change"
  />
</template>

<script>
import TranslationsMixin from '../../util/translations_mixin';

import InputBase from './base';

export default {
  name: 'DCheckbox',
  mixins: [InputBase, TranslationsMixin],
  computed: { indeterminate() { return this.value == null; } },
  methods: {
    change(newValue) {
      console.log(this.value, newValue);
    },
  },
};
</script>

<style>
th .position-checkbox-static {
  position: static !important;
  margin-left: 0 !important;
}
</style>
