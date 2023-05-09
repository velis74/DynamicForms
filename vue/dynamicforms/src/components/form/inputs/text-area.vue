<template>
  <vuetify-input
    :label="baseBinds.label"
    :messages="baseBinds.messages"
    :error-messages="baseBinds['error-messages']"
    :error-count="baseBinds['error-count']"
  >
    <div style="width: 100%;">
      <v-textarea
        :id="field.uuid"
        v-model="value"
        :type="inputType"
        variant="underlined"
        :class="field.renderParams.fieldCSSClass"
        :name="field.name"
        :placeholder="field.placeholder"

        :minlength="minLength"
        :maxlength="maxLength"
        :step="field.renderParams.step"
        :size="field.renderParams.size"

        :readonly="field.readOnly"
        :disabled="field.readOnly"
      />
    </div>
  </vuetify-input>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import TranslationsMixin from '../../util/translations-mixin';

import InputBase from './base';
import VuetifyInput from './input-vuetify.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'DTextArea',
  components: { VuetifyInput },
  mixins: [InputBase, TranslationsMixin],
  computed: {
    inputType() { return this.field.renderParams.inputType; },
    minLength() { return this.field.renderParams.minLength; },
    maxLength() { return this.field.renderParams.maxLength; },
    value: {
      get: function get() { return this.modelValue; },
      set: function set(newVal: string) { this.$emit('update:modelValue', newVal); },
    },
  },
});
</script>
