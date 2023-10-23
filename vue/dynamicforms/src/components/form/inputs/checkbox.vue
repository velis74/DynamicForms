<template>
  <v-checkbox
    v-model="boolValue"
    :indeterminate="indeterminate"
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

<script setup lang="ts">



</script>

<script lang="ts">
import _ from 'lodash';
import { defineComponent } from 'vue';

import TranslationsMixin from '../../util/translations-mixin';

import InputBase from './base';

export default /* #__PURE__ */ defineComponent({
  name: 'DCheckbox',
  mixins: [InputBase, TranslationsMixin],
  data() { return { internalValue: false as boolean | null }; },
  computed: {
    indeterminate() {
      return this.field.allowNull && (this.internalValue == null);
    },
    boolValue: {
      get() { return this.internalValue; },
      set(newVal: boolean) { console.log(this.value, newVal); },
    },
  },
  mounted() {
    if (this.value) {
      this.internalValue = true;
    } else if (this.field.allowNull && this.value == null) {
      this.internalValue = null;
    } else {
      this.internalValue = false;
    }
  },
  methods: {
    change() {
      const oldVal = _.clone(this.internalValue);
      if (oldVal === true) {
        this.internalValue = this.field.allowNull ? null : false;
      } else {
        this.internalValue = oldVal === false;
      }
      this.value = this.internalValue;
    },
  },
});
</script>
