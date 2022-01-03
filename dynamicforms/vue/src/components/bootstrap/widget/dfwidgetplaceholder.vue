<template>
  <DFWidgetBase :def="def" :data="data" :errors="errors" :show-label-or-help-text="showLabelOrHelpText">
    <div slot="input">
      <input
        :id="def.uuid"
        v-model="value"
        type="hidden"
        :class="def.render_params.field_class"
        :name="def.name"
      >
      <div class="alert alert-info">
        Table-type nested serializers not supported for direct rendering yet. Please create your own
        <b>as_component_def_table()</b> function and appropriate <b>visual component</b>.
      </div>
    </div>
  </DFWidgetBase>
</template>

<script>
import DFWidgetBase from './dfwidgetbase.vue';

export default {
  name: 'DFWidgetPlaceholder',
  components: { DFWidgetBase },
  props: {
    def: { type: Object, required: true },
    data: { type: Object, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
  },
  computed: {
    value: {
      get: function get() { return this.data[this.def.name]; },
      set: function set(newVal) {
        this.data[this.def.name] = newVal; // eslint-disable-line
      },
    },
  },
  methods: {},
};
</script>
