<template>
  <InputBase :def="def" :data="data" :errors="errors" :show-label-or-help-text="showLabelOrHelpText">
    <input
      :id="def.uuid"
      slot="input"
      v-model="value"
      :type="inputType"
      :class="def.render_params.field_class"
      :name="def.name"
      :aria-describedby="def.help_text && showLabelOrHelpText ? def.name + '-help' : null"

      :pattern="def.render_params.pattern"
      :min="def.render_params.min"
      :max="def.render_params.max"
      :step="def.render_params.step"
      :minlength="def.render_params.min_length"
      :maxlength="maxLength"
      :size="def.render_params.size"

      :readonly="def.read_only === true"
      :disabled="def.read_only === true"

      @keyup.enter="onValueConfirmed(true)"
      @input="onValueConfirmed(false)"
      @change="onValueConfirmed(false)"
    >
  </InputBase>
</template>

<script>
import InputBase from './base';

export default {
  name: 'DTextArea',
  components: { InputBase },
  props: {
    def: { type: Object, required: true },
    data: { type: Object, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
  },
  computed: {
    inputType() {
      return this.def.render_params.input_type;
    },
    maxLength() {
      return this.def.render_params.max_length || (1 << 24);
    }, // eslint-disable-line no-bitwise
    value: {
      get: function get() {
        return this.data[this.def.name];
      },
      set: function set(newVal) {
        this.data[this.def.name] = newVal; // eslint-disable-line
      },
    },
  },
  methods: {
    onValueConfirmed(doFilter) {
      this.$emit('onValueConfirmed', doFilter);
    },
  },
};
</script>
