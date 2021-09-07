<template>
  <DFWidgetBase :def="def" :data="data" :errors="errors" :show-label-or-help-text="showLabelOrHelpText">
    <input
      :id="def.uuid"
      slot="input"
      v-model="value"
      :type="def.render_params.input_type"
      :class="def.render_params.field_class"
      :name="def.name"
      :aria-describedby="def.help_text && showLabelOrHelpText ? def.name + '-help' : null"
      :placeholder="def.placeholder"

      :pattern="def.render_params.pattern"
      :min="def.render_params.min"
      :max="def.render_params.max"
      :step="def.render_params.step"
      :minlength="def.render_params.minlength"
      :maxlength="def.render_params.maxlength"
      :size="def.render_params.size"

      @keyup.enter="onValueConfirmed(true)"
      @input="onValueConfirmed(false)"
      @change="onValueConfirmed(false)"
    >
  </DFWidgetBase>
</template>

<script>
import DFWidgetBase from './dfwidgetbase.vue';

export default {
  name: 'DFWidgetInput',
  components: { DFWidgetBase },
  props: {
    def: { type: Object, required: true },
    data: { type: Object, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
  },
  computed: {
    value: {
      get: () => this.data[this.def.name],
      set: (newVal) => {
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

<style scoped>

</style>
