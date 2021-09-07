<template>
  <input v-if="isHidden" type="hidden" :name="def.name" :value="data[def.name]">
  <div v-else :id="'container-' + def.uuid" :class="def.render_params.container_class">
    <slot name="error">
      <small v-if="getErrorText" :id="def.name + '-err'" class="form-text text-danger">{{ getErrorText }}</small>
    </slot>
    <DFWidgetBaseLabel v-if="labelAfterElement === false && showLabelOrHelpText" :data="data" :def="def"/>
    <slot name="input"/>
    <DFWidgetBaseLabel v-if="labelAfterElement && showLabelOrHelpText" :data="data" :def="def"/>
    <slot name="help">
      <small
        v-if="def.help_text && showLabelOrHelpText"
        :id="def.name + '-help'"
        class="form-text text-muted"
      >{{ def.help_text }}</small>
    </slot>
  </div>
</template>

<script>
import DisplayMode from '../../../logic/displayMode';

import DFWidgetBaseLabel from './dfwidgetbaselabel.vue';

export default {
  name: 'DFWidgetBase',
  components: { DFWidgetBaseLabel },
  props: {
    def: { type: Object, required: true },
    data: { type: Object, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
  },
  computed: {
    isHidden() {
      return this.def.visibility.form === DisplayMode.HIDDEN;
    },
    labelAfterElement() {
      return this.def.render_params.label_after_element;
    },
    getErrorText() {
      try {
        if (this.errors && this.errors[this.def.name]) return this.errors[this.def.name];
        // eslint-disable-next-line no-empty
      } catch (e) {}
      return '';
    },
  },
};
</script>

<style scoped>

</style>
